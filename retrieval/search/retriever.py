"""
Retriever module.

Generates query embeddings and retrieves the
most relevant document chunks from PGVector.
"""

from retrieval.config.settings import Settings
from retrieval.embeddings.embedder import Embedder


class Retriever:
    """
    Handles semantic retrieval.
    """

    def __init__(self):
        self.embedder = Embedder()

    def retrieve(
        self,
        query: str,
        top_k: int = Settings.TOP_K,
    ) -> list:
        """
        Retrieve the most relevant chunks for a user query.

        Args:
            query (str): User query.
            top_k (int): Number of results to retrieve.

        Returns:
            list: Top-k retrieved document chunks.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = self.embedder.encode(query)

        from backend.app.services.vector.pinecone_service import PineconeService
        results = PineconeService.query_vectors(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results