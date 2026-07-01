"""
Test for loading Team A's JSONL dataset
and verifying the embedding pipeline.
"""

from retrieval.embeddings.embedder import Embedder
from retrieval.pipelines.json_loader import JSONLoader

# Team A output file
FILE_PATH = "chunked_documents.jsonl"


def main():
    documents = JSONLoader.load(FILE_PATH)

    print("=" * 60)
    print(f"Total Chunks : {len(documents)}")
    print("=" * 60)

    first_doc = documents[0]

    print("\nFirst Chunk:\n")
    print(first_doc["page_content"][:300] + "...")

    print("\nMetadata:\n")
    for key, value in first_doc["metadata"].items():
        print(f"{key}: {value}")

    print("\nGenerating embedding...\n")

    embedder = Embedder()

    embedding = embedder.encode(first_doc["page_content"])

    print(f"Embedding Dimension : {len(embedding)}")
    print("Embedding generated successfully.")


if __name__ == "__main__":
    main()