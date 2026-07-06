"""
Embedding generation module.

This module generates embeddings for document chunks
and user queries using the shared embedding model.
"""

from typing import List

from retrieval.embeddings.model import EmbeddingModel


class Embedder:
    """
    Handles embedding generation using the shared embedding model.
    """

    def __init__(self):
        """Initialize the embedder."""
        pass

    @property
    def _model(self):
        """Lazy load the embedding model."""
        return EmbeddingModel.get_model()

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

        embedding = self._model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

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

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()