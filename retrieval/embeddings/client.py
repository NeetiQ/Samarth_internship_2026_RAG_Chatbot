import httpx
import time
import logging
from typing import List, Dict, Any
from retrieval.config.settings import Settings

logger = logging.getLogger("legal-rag-client")

class EmbeddingClient:
    """
    Lightweight, resilient HTTP client for interacting with the
    external Hugging Face Embedding Service.
    """
    def __init__(self):
        self.url = Settings.EMBEDDING_SERVICE_URL.rstrip('/')
        self.api_key = Settings.EMBEDDING_SERVICE_API_KEY
        self.timeout = 30.0
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self._client = None

    def _get_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(timeout=self.timeout)
        return self._client

    def close(self):
        if self._client and not self._client.is_closed:
            self._client.close()

    def _post_with_retry(self, path: str, payload: dict) -> httpx.Response:
        client = self._get_client()
        url = f"{self.url}{path}"
        
        max_retries = 2
        delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                response = client.post(url, json=payload, headers=self.headers)
                if response.status_code == 200:
                    return response
                
                if 400 <= response.status_code < 500:
                    response.raise_for_status()
                    
                logger.warning(
                    f"Embedding request failed with status {response.status_code}. "
                    f"Attempt {attempt + 1}/{max_retries + 1}."
                )
            except Exception as e:
                logger.warning(
                    f"Embedding request error: {e}. "
                    f"Attempt {attempt + 1}/{max_retries + 1}."
                )
            
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
                
        raise httpx.HTTPStatusError(
            message="Embedding service unavailable after retries.",
            request=httpx.Request("POST", url),
            response=httpx.Response(503)
        )

    def get_health(self) -> Dict[str, Any]:
        """Query health status of the embedding service."""
        client = self._get_client()
        url = f"{self.url}/health"
        try:
            response = client.get(url, timeout=5.0)
            if response.status_code == 200:
                return response.json()
            return {"status": "unhealthy", "status_code": response.status_code}
        except Exception as e:
            logger.error(f"Failed to fetch embedding service health: {e}")
            return {"status": "unhealthy", "error": str(e)}

    def encode(self, text: str) -> List[float]:
        """Generate embedding for a single text chunk or query."""
        payload = {"text": text}
        try:
            response = self._post_with_retry("/embed/query", payload)
            data = response.json()
            return data["embedding"]
        except Exception as e:
            logger.exception(f"Error encoding query: {e}")
            raise RuntimeError(f"Embedding service error: {e}") from e

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of document chunks in a single request."""
        payload = {"texts": texts}
        try:
            response = self._post_with_retry("/embed/document", payload)
            data = response.json()
            return data["embeddings"]
        except Exception as e:
            logger.exception(f"Error batch encoding documents: {e}")
            raise RuntimeError(f"Embedding service error: {e}") from e
