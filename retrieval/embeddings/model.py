"""
Embedding model loader.

Loads the SentenceTransformer model only once
and reuses it throughout the application.
"""

from typing import Optional

from sentence_transformers import SentenceTransformer

from retrieval.config.settings import Settings


class EmbeddingModel:
    """Singleton loader for the embedding model."""

    _model: Optional[SentenceTransformer] = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """
        Returns the shared embedding model instance.
        """

        if cls._model is None:
            print(f"Loading embedding model: {Settings.EMBEDDING_MODEL}")

            cls._model = SentenceTransformer(
                Settings.EMBEDDING_MODEL
            )

        return cls._model