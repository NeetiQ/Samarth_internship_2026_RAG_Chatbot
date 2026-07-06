"""
Embedding model loader.

Loads the SentenceTransformer model only once
and reuses it throughout the application.
"""

from typing import Optional

from retrieval.config.settings import Settings


class EmbeddingModel:
    """Singleton loader for the embedding model."""

    _model: Optional[object] = None

    @classmethod
    def get_model(cls) -> object:
        """
        Returns the shared embedding model instance.
        """
        if cls._model is None:
            import sys
            import os
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
            from backend.app.core.diagnostic_logger import Profiler

            with Profiler("Loading SentenceTransformer"):
                from sentence_transformers import SentenceTransformer
                
                print("=" * 60)
                print(f"Loading Embedding Model : {Settings.EMBEDDING_MODEL}")
                print(f"Embedding Dimension     : {Settings.EMBEDDING_DIMENSION}")
                print("=" * 60)

                try:
                    cls._model = SentenceTransformer(
                        Settings.EMBEDDING_MODEL
                    )
                    print("Embedding model loaded successfully.\n")

                except Exception as error:
                    import logging
                    logging.getLogger("legal-rag-diagnostics").exception(f"Failed to load embedding model: {error}")
                    raise RuntimeError(
                        f"Failed to load embedding model: {error}"
                    ) from error

        return cls._model