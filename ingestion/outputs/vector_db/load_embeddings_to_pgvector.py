import os
import json
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/legal_rag").replace(
    "postgresql+asyncpg://", "postgresql://"
)
INPUT_FILE = Path(os.getenv("EMBEDDED_DOCUMENTS_PATH", REPO_ROOT / "embedded_documents.jsonl"))


def vector_to_sql(embedding):
    return "[" + ",".join(str(x) for x in embedding) + "]"


def main():
    if not INPUT_FILE.is_file():
        print(f"Input file not found: {INPUT_FILE}", file=sys.stderr)
        print("Run: python backend/scripts/generate_embeddings.py", file=sys.stderr)
        return 1

    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()

    inserted = 0

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)

            page_content = record["page_content"]
            metadata = record.get("metadata", {})
            embedding = record["embedding"]
            chunk_id = metadata.get("chunk_id")

            if not chunk_id:
                continue

            cur.execute(
                """
                INSERT INTO legal_chunks (
                    chunk_id,
                    page_content,
                    metadata,
                    embedding
                )
                VALUES (%s, %s, %s::jsonb, %s::vector)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    page_content = EXCLUDED.page_content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding;
                """,
                (
                    chunk_id,
                    page_content,
                    json.dumps(metadata),
                    vector_to_sql(embedding),
                ),
            )

            inserted += 1

            if inserted % 500 == 0:
                conn.commit()
                print(f"Inserted {inserted} records...")

    conn.commit()

    cur.close()
    conn.close()

    print(f"Done. Total records loaded: {inserted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
