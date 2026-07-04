"""
Retriever module.

Generates query embeddings and retrieves the
most relevant document chunks from Pinecone.
"""

from retrieval.config.settings import Settings
import builtins
def _trace(msg):
    builtins.print(msg, flush=True)

_trace("retriever.py: Importing Embedder")
from retrieval.embeddings.embedder import Embedder
_trace("retriever.py: Importing PineconeStore")
from retrieval.vectordb.pinecone_store import PineconeStore


class Retriever:
    """
    Orchestrates semantic search and hybrid search.
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

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results