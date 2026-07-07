from typing import List

from retrieval.embeddings.client import EmbeddingClient


class Embedder:
    """
    Handles embedding generation using the external embedding service.
    """

    def __init__(self):
        """Initialize the embedder with the shared HTTP client."""
        self.client = EmbeddingClient()

    def encode(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text.

        Args:
            text (str): Input text.

        Returns:
            List[float]: Embedding vector.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        return self.client.encode(text)

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts (List[str]): List of input texts.

        Returns:
            List[List[float]]: List of embedding vectors.
        """
        if not texts:
            raise ValueError("Input text list cannot be empty.")

        return self.client.encode_batch(texts)