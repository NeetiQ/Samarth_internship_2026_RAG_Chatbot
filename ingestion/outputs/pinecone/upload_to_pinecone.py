import json
import uuid
import time
import httpx
from pinecone import Pinecone

from ingestion.outputs.pinecone.embedding_config import *

_index = None

class EmbeddingClient:
    """
    Independent, lightweight HTTP client for Team A ingestion.
    """
    def __init__(self):
        self.url = EMBEDDING_SERVICE_URL.rstrip('/')
        self.api_key = EMBEDDING_SERVICE_API_KEY
        self.timeout = 60.0
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def encode_batch(self, texts: list) -> list:
        max_retries = 2
        delay = 1.0
        url = f"{self.url}/embed/document"
        
        for attempt in range(max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(url, json={"texts": texts}, headers=self.headers)
                    if response.status_code == 200:
                        return response.json()["embeddings"]
                    if 400 <= response.status_code < 500:
                        response.raise_for_status()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
        raise RuntimeError("Embedding service failed after retries.")


def get_index():
    """
    Connect to Pinecone only once.
    """
    global _index

    if _index is None:
        print("Connecting to Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = pc.Index(PINECONE_INDEX_NAME)
        print("Connected to Pinecone.")

    return _index


def upload_chunks(
    chunk_file: str,
    batch_size: int = 500
):
    """
    Upload chunked documents to Pinecone.

    Args:
        chunk_file (str):
            Path to chunked_documents_new.jsonl

        batch_size (int):
            Pinecone upload batch size

    Returns:
        dict
    """
    index = get_index()
    client = EmbeddingClient()

    print(f"\nReading chunks from {chunk_file}")

    chunks = []
    with open(chunk_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            chunks.append(json.loads(line))

    total_chunks = len(chunks)
    print(f"Total chunks loaded: {total_chunks}")

    # Generate embeddings in batches
    embed_batch_size = 128
    embeddings = []
    
    for i in range(0, total_chunks, embed_batch_size):
        batch_chunks = chunks[i:i + embed_batch_size]
        texts = [c["page_content"] for c in batch_chunks]
        print(f"Generating embeddings for chunks {i} to {min(i + embed_batch_size, total_chunks)}...")
        batch_embeddings = client.encode_batch(texts)
        embeddings.extend(batch_embeddings)

    batch = []
    total_uploaded = 0

    for idx, chunk in enumerate(chunks):
        text = chunk["page_content"]
        embedding = embeddings[idx]
        metadata = chunk.get("metadata", {})

        batch.append(
            {
                "id": metadata.get(
                    "chunk_id",
                    str(uuid.uuid4())
                ),
                "values": embedding,
                "metadata": {
                    "text": text,
                    "chunk_id": metadata.get("chunk_id", ""),
                    "source": metadata.get("source", ""),
                    "title": metadata.get("title", ""),
                    "case_id": metadata.get("case_id", ""),
                    "court": metadata.get("court", ""),
                    "decision_date": metadata.get(
                        "decision_date",
                        ""
                    ),
                    "citation": metadata.get(
                        "citation",
                        ""
                    ),
                    "judge": metadata.get(
                        "judge",
                        ""
                    ),
                    "year": metadata.get(
                        "year",
                        ""
                    ),
                },
            }
        )

        if len(batch) >= batch_size:
            index.upsert(vectors=batch)
            total_uploaded += len(batch)
            print(f"Uploaded {total_uploaded} chunks...")
            batch = []

    if batch:
        index.upsert(vectors=batch)
        total_uploaded += len(batch)

    print(f"\nUpload completed successfully. Total uploaded: {total_uploaded}")
    return {
        "status": "success",
        "uploaded": total_uploaded,
    }


if __name__ == "__main__":
    result = upload_chunks(
        "chunked_documents_new.jsonl"
    )
    print(result)