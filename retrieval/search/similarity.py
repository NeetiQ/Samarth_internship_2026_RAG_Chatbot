"""
Similarity utilities for the Retrieval module.
"""

from typing import List


class Similarity:
    """
    Utility class for similarity calculations.
    """

    TOP_K = 5

    @staticmethod
    def cosine_distance() -> str:
        """
        Returns the similarity metric used in retrieval.

        Returns:
            str
        """
        return "cosine"

    @staticmethod
    def top_k() -> int:
        """
        Returns the number of chunks retrieved.

        Returns:
            int
        """
        return Similarity.TOP_K

    @staticmethod
    def validate_embedding(vector: List[float]) -> bool:
        """
        Validate an embedding vector.

        Args:
            vector (List[float])

        Returns:
            bool
        """

        return (
            isinstance(vector, list)
            and len(vector) > 0
            and all(isinstance(x, (float, int)) for x in vector)
        )