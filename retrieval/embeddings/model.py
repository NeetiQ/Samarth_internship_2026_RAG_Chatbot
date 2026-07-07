"""
Embedding model loader (Stubbed).

Model loading has been moved to the external Hugging Face Embedding Service.
Local embedding loading is disabled to prevent memory bottlenecks.
"""

class EmbeddingModel:
    """Stub for the singleton embedding model loader."""

    @classmethod
    def get_model(cls) -> object:
        """
        Raises RuntimeError because local model loading is deprecated.
        """
        raise RuntimeError(
            "Local embedding model loading is disabled. "
            "Please use retrieval.embeddings.client.EmbeddingClient instead."
        )