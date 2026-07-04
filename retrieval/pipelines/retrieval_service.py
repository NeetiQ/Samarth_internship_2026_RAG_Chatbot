"""
Retrieval service for indexing documents.
"""

from retrieval.embeddings.embedder import Embedder
from retrieval.pipelines.json_loader import JSONLoader
from retrieval.vectordb.pinecone_store import PineconeStore


class RetrievalService:

    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = PineconeStore()

    def ingest_documents(self, jsonl_path: str):

        documents = JSONLoader.load(jsonl_path)

        batch_size = 64
        vectors = []

        print(f"Total Documents: {len(documents)}")

        for i in range(0, len(documents), batch_size):

            batch = documents[i:i + batch_size]

            texts = [
                doc["page_content"]
                for doc in batch
            ]

            embeddings = self.embedder.encode_batch(texts)

            for document, embedding in zip(batch, embeddings):

                vectors.append(
                    {
                        "id": document["metadata"]["chunk_id"],
                        "values": embedding,
                        "metadata": {
                            **document["metadata"],
                            "page_content": document["page_content"],
                        },
                    }
                )

            print(
                f"Embeddings Generated: "
                f"{min(i + batch_size, len(documents))}/{len(documents)}"
            )

        return vectors

    def index_documents(self, jsonl_path: str):

        vectors = self.ingest_documents(jsonl_path)

        upsert_batch = 500

        for i in range(0, len(vectors), upsert_batch):

            self.vector_store.upsert(
                vectors[i:i + upsert_batch]
            )

            print(
                f"Uploaded: "
                f"{min(i + upsert_batch, len(vectors))}/{len(vectors)}"
            )

        print("\nIndexing Completed Successfully.")

        return vectors