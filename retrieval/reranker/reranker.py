"""
Cross-Encoder Reranker.

Loads the reranker model only once and reranks
retrieved chunks based on query relevance.
"""

from typing import List, Dict

from retrieval.config.settings import Settings


class Reranker:
    """Singleton CrossEncoder reranker."""

    _model = None

    @classmethod
    def get_model(cls):
        """Load reranker model only once."""

        if cls._model is None:
            print("=" * 60)
            print(f"Loading Reranker Model : {Settings.RERANKER_MODEL}")
            print("=" * 60)

            from sentence_transformers import CrossEncoder
            cls._model = CrossEncoder(Settings.RERANKER_MODEL)

            print("Reranker loaded successfully.\n")

        return cls._model

    @classmethod
    def rerank(
        cls,
        query: str,
        results: List[Dict]
    ) -> List[Dict]:
        """
        Rerank retrieved chunks using a CrossEncoder.
        """

        if (
            not Settings.RERANKER_ENABLED
            or len(results) == 0
        ):
            return results

        model = cls.get_model()

        sentence_pairs = [
            (
                query,
                result.get("page_content", "")
            )
            for result in results
        ]

        scores = model.predict(sentence_pairs)

        # Pair each score with its result
        ranked_results = list(zip(scores, results))

        # Sort by reranker score
        ranked_results.sort(
            key=lambda x: x[0],
            reverse=True
        )

        # Return only the original result dictionaries
        return [
            result
            for _, result in ranked_results[:Settings.FINAL_TOP_K]
        ]