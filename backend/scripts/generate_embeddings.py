#!/usr/bin/env python3
"""Generate embedded_documents.jsonl from chunked_documents.jsonl at repo root."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from retrieval.embeddings.client import EmbeddingClient

load_dotenv(REPO_ROOT / ".env")

CHUNKED_PATH = Path(os.getenv("CHUNKED_DOCUMENTS_PATH", REPO_ROOT / "chunked_documents.jsonl"))
EMBEDDED_PATH = Path(os.getenv("EMBEDDED_DOCUMENTS_PATH", REPO_ROOT / "embedded_documents.jsonl"))
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "64"))


def load_chunks(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("page_content", "").strip():
                records.append(record)
    return records


def main() -> int:
    if not CHUNKED_PATH.is_file():
        print(f"Chunked file not found: {CHUNKED_PATH}", file=sys.stderr)
        return 1

    print(f"Loading chunks from {CHUNKED_PATH}...")
    records = load_chunks(CHUNKED_PATH)
    print(f"Total chunks: {len(records)}")

    print("Initializing EmbeddingClient...")
    client = EmbeddingClient()
    texts = [record["page_content"] for record in records]

    print("Generating embeddings in batches...")
    embeddings = []
    
    for i in range(0, len(texts), BATCH_SIZE):
        print(f"Processing batch {i//BATCH_SIZE + 1}...")
        batch_texts = texts[i:i+BATCH_SIZE]
        batch_embeddings = client.encode_batch(batch_texts)
        embeddings.extend(batch_embeddings)

    EMBEDDED_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing {EMBEDDED_PATH}...")
    with EMBEDDED_PATH.open("w", encoding="utf-8") as file:
        for record, embedding in zip(records, embeddings):
            output = {
                "page_content": record["page_content"],
                "metadata": record.get("metadata", {}),
                "embedding": embedding.tolist(),
            }
            file.write(json.dumps(output, ensure_ascii=False) + "\n")

    print(f"Done. Wrote {len(records)} records ({len(embeddings[0])}-dim vectors).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
