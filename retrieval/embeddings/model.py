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
        import builtins
        builtins.print("EmbeddingModel.get_model: Called", flush=True)


        if cls._model is None:
            builtins.print("EmbeddingModel.get_model: Model is None, initializing...", flush=True)
            print("=" * 60)
            print(f"Loading Embedding Model : {Settings.EMBEDDING_MODEL}")
            print(f"Embedding Dimension     : {Settings.EMBEDDING_DIMENSION}")
            print("=" * 60)

            try:
                builtins.print("EmbeddingModel.get_model: calling SentenceTransformer", flush=True)
                cls._model = SentenceTransformer(
                    Settings.EMBEDDING_MODEL
                )
                builtins.print("EmbeddingModel.get_model: SentenceTransformer loaded", flush=True)
                print("Embedding model loaded successfully.\n")

            except Exception as error:
                raise RuntimeError(
                    f"Failed to load embedding model: {error}"
                ) from error

        builtins.print("EmbeddingModel.get_model: returning model", flush=True)
        return cls._model