"""
Application configuration.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    # ==========================================
    # Pinecone Configuration
    # ==========================================

    PINECONE_API_KEY = os.getenv("pcsk_4iBwWL_GZyBgx7zBHZxrVwHzmGFXDTLAuCUjC7esBsaz8gxbxpmrxaffaqCAq9XYFB9PSJ", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "legal-rag")
    PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

    # ==========================================
    # Embedding Configuration
    # ==========================================

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    EMBEDDING_DIMENSION = int(
        os.getenv("EMBEDDING_DIMENSION", 384)
    )

    # ==========================================
    # Retrieval Configuration
    # ==========================================

    TOP_K = int(os.getenv("TOP_K", 5))

    SIMILARITY = os.getenv(
        "SIMILARITY",
        "cosine",
    )

    # ==========================================
    # Chunking Configuration
    # ==========================================

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 600)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 100)
    )