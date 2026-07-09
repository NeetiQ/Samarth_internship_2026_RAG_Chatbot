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
<<<<<<< HEAD
        raise RuntimeError(
            "Local embedding model loading is disabled. "
            "Please use retrieval.embeddings.client.EmbeddingClient instead."
        )
=======
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
>>>>>>> staging
