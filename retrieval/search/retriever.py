"""
Retriever module.

Generates query embeddings, retrieves relevant
document chunks from Pinecone and reranks them.
"""

from retrieval.config.settings import Settings

import builtins

from retrieval.embeddings.embedder import Embedder
from retrieval.reranker.reranker import Reranker
from retrieval.vectordb.pinecone_store import PineconeStore


def _trace(msg):
    builtins.print(msg, flush=True)


_trace("retriever.py: Importing Embedder")
_trace("retriever.py: Importing Reranker")
_trace("retriever.py: Importing PineconeStore")


class Retriever:
    """
    Handles semantic retrieval and reranking.
    """

    def __init__(self):
        _trace("Retriever.__init__: Instantiating Embedder")
        self.embedder = Embedder()

        _trace("Retriever.__init__: Instantiating PineconeStore")
        self.vector_store = PineconeStore()

        _trace("Retriever.__init__: Done")

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
            list: Final reranked chunks.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        # Generate query embedding
        query_embedding = self.embedder.encode(query)

        # Retrieve from Pinecone
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