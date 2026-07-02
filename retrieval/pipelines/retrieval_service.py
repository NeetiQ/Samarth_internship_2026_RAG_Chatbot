"""
Retrieval service for indexing documents.
"""

from retrieval.embeddings.embedder import Embedder
from retrieval.pipelines.json_loader import JSONLoader


class RetrievalService:
    """
    Handles document ingestion and indexing.
    """

    def __init__(self):
        self.embedder = Embedder()

    def ingest_documents(self, jsonl_path: str):
        """
        Load documents and generate embeddings.

        Args:
            jsonl_path (str): Path to the JSONL file.

        Returns:
            list: Documents with embeddings.
        """

        documents = JSONLoader.load(jsonl_path)

        indexed_documents = []

        for document in documents:

            embedding = self.embedder.encode(
                document.get("page_content", "")
            )

            indexed_documents.append(
                {
                    "id": document["metadata"]["chunk_id"],  # Pinecone requires 'id'
                    "values": embedding,                     # Pinecone requires 'values'
                    "metadata": {
                        **document["metadata"],
                        "page_content": document.get("page_content", "")
                    }
                }
            )

        return indexed_documents

    def index_documents(self, jsonl_path: str):
        """
        Generate embeddings and store them in PGVector.

        Args:
            jsonl_path (str): Path to the JSONL file.

        Returns:
            list: Indexed documents.
        """

        documents = self.ingest_documents(jsonl_path)

        from backend.app.services.vector.pinecone_service import PineconeService
        PineconeService.upsert_vectors(documents)

        return documents