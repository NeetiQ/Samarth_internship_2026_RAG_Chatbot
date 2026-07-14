"""
HTTP Reranker Adapter.

Replaces the local CrossEncoder with a remote call to POST /rerank on the
Hugging Face Inference Service. The public interface (Reranker.rerank) is
identical to the old implementation so retriever.py requires zero changes.

Fallback behaviour: if the remote service is unavailable, the original
Pinecone-ranked results are returned unchanged — the pipeline never crashes.
"""

import logging
from typing import List, Dict

from retrieval.config.settings import Settings
from retrieval.embeddings.client import EmbeddingClient

logger = logging.getLogger("legal-rag-reranker")


class Reranker:
    """HTTP adapter for the remote reranker service."""

    # Shared client instance — connection pool is reused across requests
    _client: EmbeddingClient = None

    @classmethod
    def _get_client(cls) -> EmbeddingClient:
        if cls._client is None:
            cls._client = EmbeddingClient()
        return cls._client

    @classmethod
    def rerank(
        cls,
        query: str,
        results: List[Dict],
    ) -> List[Dict]:
        """
        Rerank retrieved chunks using the remote HF reranker service.

        Args:
            query:   User query string.
            results: Retrieved document chunks from Pinecone, each a dict
                     with at least a "page_content" key.

        Returns:
            Top FINAL_TOP_K chunks sorted by reranker score (descending).
            Falls back to original Pinecone ordering if the service fails.
        """
        if not Settings.RERANKER_ENABLED or len(results) == 0:
            return results

        documents = [r.get("page_content", "") for r in results]

        try:
            client = cls._get_client()
            ranked = client.rerank(query=query, documents=documents)

            # ranked is [{index, score}, ...] already sorted descending by the service
            reranked_results = [results[item["index"]] for item in ranked]

            return reranked_results[: Settings.FINAL_TOP_K]

        except Exception as e:
            logger.error(
                f"Reranker service unavailable — falling back to Pinecone ranking. "
                f"Error: {e}"
            )
            # Graceful degradation: return original Pinecone results unchanged
            return results[: Settings.FINAL_TOP_K]