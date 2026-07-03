import json
import uuid

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from ingestion.outputs.pinecone.embedding_config import *

_model = None
_index = None


def get_model():
    """
    Load embedding model only once.
    """
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded.")

    return _model


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

    model = get_model()
    index = get_index()

    batch = []
    total_uploaded = 0

    print(f"\nReading chunks from {chunk_file}")

    with open(chunk_file, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            chunk = json.loads(line)

            text = chunk["page_content"]

            embedding = model.encode(text).tolist()

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

                print(
                    f"Uploaded {total_uploaded} chunks..."
                )

                batch = []

    if batch:

        index.upsert(vectors=batch)

        total_uploaded += len(batch)

    print(
        f"\nUpload completed successfully."
    )

    print(
        f"Total uploaded: {total_uploaded}"
    )

    return {
        "status": "success",
        "uploaded": total_uploaded,
    }


if __name__ == "__main__":

    result = upload_chunks(
        "chunked_documents_new.jsonl"
    )

    print(result)