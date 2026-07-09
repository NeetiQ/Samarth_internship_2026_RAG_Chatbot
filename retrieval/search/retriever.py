"""
Retriever module.

Generates query embeddings, retrieves relevant
document chunks from Pinecone and reranks them.
"""

from retrieval.config.settings import Settings
from retrieval.embeddings.embedder import Embedder
from retrieval.reranker.reranker import Reranker
from retrieval.vectordb.pinecone_store import PineconeStore


class Retriever:
    """
    Handles semantic retrieval and reranking.
    """

    def __init__(self):
        """Initialize embedder and vector store."""
        self.embedder = Embedder()
        self.vector_store = PineconeStore()

    def retrieve(
        self,
        query: str,
        top_k: int = Settings.TOP_K,
    ) -> list:
        """
        Retrieve and rerank the most relevant chunks.

        Args:
            query (str): User query.
            top_k (int): Number of chunks to retrieve.

        Returns:
            list: Final reranked document chunks.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        # Generate query embedding using the external embedding service
        query_embedding = self.embedder.encode(query)

        # Retrieve candidate chunks from Pinecone
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # Apply reranking if enabled
        if Settings.RERANKER_ENABLED:
            results = Reranker.rerank(
                query=query,
                results=results,
            )

        return results