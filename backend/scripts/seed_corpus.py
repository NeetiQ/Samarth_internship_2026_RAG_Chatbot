#!/usr/bin/env python3
"""Seed shared legal corpus from embedded_documents.jsonl into Postgres."""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import psycopg
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

EMBEDDED_PATH = Path(os.getenv("EMBEDDED_DOCUMENTS_PATH", REPO_ROOT / "embedded_documents.jsonl"))
CHUNKED_PATH = Path(os.getenv("CHUNKED_DOCUMENTS_PATH", REPO_ROOT / "chunked_documents.jsonl"))
BATCH_SIZE = int(os.getenv("SEED_BATCH_SIZE", "500"))


def sync_database_url() -> str:
    url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/legal_rag")
    return url.replace("postgresql+asyncpg://", "postgresql://")


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def vector_to_sql(embedding: list[float]) -> str:
    return "[" + ",".join(str(x) for x in embedding) + "]"


def ensure_embedded_file() -> Path:
    if EMBEDDED_PATH.is_file():
        return EMBEDDED_PATH

    if CHUNKED_PATH.is_file() and os.getenv("GENERATE_EMBEDDINGS_ON_SEED", "").lower() in {"1", "true", "yes"}:
        print("Embedded file missing — generating from chunked file (this may take a while)...")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "backend/scripts/generate_embeddings.py")],
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError("Failed to generate embeddings from chunked file")
        return EMBEDDED_PATH

    raise FileNotFoundError(
        f"Embedded corpus not found at {EMBEDDED_PATH}. "
        f"Run: python backend/scripts/generate_embeddings.py "
        f"or set GENERATE_EMBEDDINGS_ON_SEED=true"
    )


def load_records(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            records.append(json.loads(line))
    return records


def seed(records: list[dict]) -> None:
    conn = psycopg.connect(sync_database_url())
    conn.autocommit = False

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM legal_chunks")
        existing = cur.fetchone()[0]
        if existing > 0:
            print(f"Corpus already seeded ({existing} chunks). Skipping.")
            conn.close()
            return

        doc_id_map: dict[str, int] = {}
        unique_docs: dict[str, dict] = {}

        for record in records:
            metadata = record.get("metadata") or {}
            doc_key = metadata.get("doc_id") or metadata.get("case_id") or metadata.get("chunk_id", "").rsplit("_", 1)[0]
            if doc_key and doc_key not in unique_docs:
                unique_docs[doc_key] = metadata

        print(f"Creating {len(unique_docs)} shared document records...")
        for doc_key, metadata in unique_docs.items():
            cur.execute(
                """
                INSERT INTO documents (
                    title, filename, file_type, court, case_number,
                    judgment_date, source, language, is_shared, user_id,
                    created_at, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true, NULL, now(), now())
                RETURNING id
                """,
                (
                    metadata.get("title") or doc_key,
                    f"{metadata.get('source') or doc_key}.pdf",
                    "application/pdf",
                    metadata.get("court"),
                    metadata.get("case_id") or doc_key,
                    parse_date(metadata.get("decision_date")),
                    metadata.get("source") or metadata.get("path"),
                    "en",
                ),
            )
            doc_id_map[doc_key] = cur.fetchone()[0]

        print(f"Inserting {len(records)} chunks...")
        inserted = 0
        for record in records:
            metadata = record.get("metadata") or {}
            chunk_id = metadata.get("chunk_id")
            if not chunk_id:
                continue

            doc_key = metadata.get("doc_id") or metadata.get("case_id") or chunk_id.rsplit("_", 1)[0]
            document_id = doc_id_map.get(doc_key)

            cur.execute(
                """
                INSERT INTO legal_chunks (chunk_id, document_id, page_content, metadata, embedding, created_at)
                VALUES (%s, %s, %s, %s::jsonb, %s::vector, now())
                ON CONFLICT (chunk_id) DO UPDATE SET
                    document_id = EXCLUDED.document_id,
                    page_content = EXCLUDED.page_content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding
                """,
                (
                    chunk_id,
                    document_id,
                    record["page_content"],
                    json.dumps(metadata),
                    vector_to_sql(record["embedding"]),
                ),
            )
            inserted += 1
            if inserted % BATCH_SIZE == 0:
                conn.commit()
                print(f"  ... {inserted} chunks inserted")

    conn.commit()
    conn.close()
    print(f"Corpus seed complete: {inserted} chunks, {len(unique_docs)} documents.")


def main() -> int:
    if os.getenv("SEED_CORPUS", "true").lower() not in {"1", "true", "yes"}:
        print("SEED_CORPUS disabled — skipping corpus seed.")
        return 0

    try:
        embedded_path = ensure_embedded_file()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Loading embedded corpus from {embedded_path}...")
    records = load_records(embedded_path)
    if not records:
        print("No records found in embedded file.", file=sys.stderr)
        return 1

    seed(records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
