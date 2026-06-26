"""
Retrieval service for indexing documents.
"""

from retrieval.embeddings.embedder import Embedder
from retrieval.pipelines.json_loader import JSONLoader
from retrieval.vectordb.pgvector_store import PGVectorStore


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
                    "chunk_id": document["metadata"]["chunk_id"],
                    "page_content": document.get("page_content", ""),
                    "metadata": document["metadata"],
                    "embedding": embedding,
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

        PGVectorStore.insert_embeddings(documents)

        return documents