"""
Pinecone Integration Service for Backend.
"""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from app.core.settings import get_settings
import logging

logger = logging.getLogger("legal-rag.pinecone")
settings = get_settings()

class PineconeService:
    """
    Centralized Pinecone integration service.
    Handles initializing, upserting, querying, and deleting vectors.
    """

    def __init__(self):
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = settings.PINECONE_INDEX
            self.index = self.pc.Index(self.index_name)
            self.namespace = settings.PINECONE_NAMESPACE
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def upsert_vectors(vectors: List[Dict[str, Any]], namespace: Optional[str] = None) -> None:
        """
        Upsert document vectors into Pinecone.

        Args:
            vectors (List[Dict]): List of dictionaries with 'id', 'values', and 'metadata'.
            namespace (str, optional): Target namespace.
        """
        svc = PineconeService.get_instance()
        target_namespace = namespace or svc.namespace

        try:
            # Batch upsert logic (Pinecone handles up to 1000 vectors per request usually)
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                svc.index.upsert(vectors=batch, namespace=target_namespace)
            logger.info(f"✅ Upserted {len(vectors)} embeddings to Pinecone namespace '{target_namespace}'.")
        except Exception as e:
            logger.error(f"Error upserting vectors to Pinecone: {e}")
            raise

    @staticmethod
    def query_vectors(query_embedding: List[float], top_k: int = 5, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query vectors from Pinecone.

        Args:
            query_embedding (List[float]): The vector to search for.
            top_k (int): Number of top matches to return.
            namespace (str, optional): Target namespace.

        Returns:
            List[Dict]: List of match dictionaries containing 'id', 'score', and 'metadata'.
        """
        svc = PineconeService.get_instance()
        target_namespace = namespace or svc.namespace

        try:
            response = svc.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=target_namespace
            )
            
            results = []
            for match in response.get('matches', []):
                results.append({
                    "chunk_id": match.get("id"),
                    "score": match.get("score"),
                    "metadata": match.get("metadata", {}),
                    "page_content": match.get("metadata", {}).get("page_content", "") 
                })
            return results
        except Exception as e:
            logger.error(f"Error querying vectors from Pinecone: {e}")
            raise

    @staticmethod
    def check_health() -> bool:
        """
        Check if Pinecone index is reachable.
        """
        try:
            svc = PineconeService.get_instance()
            stats = svc.index.describe_index_stats()
            return stats is not None
        except Exception as e:
            logger.error(f"Pinecone health check failed: {e}")
            return False
