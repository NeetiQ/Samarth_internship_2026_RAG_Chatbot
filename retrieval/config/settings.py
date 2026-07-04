"""
Application configuration.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    # ==========================================
    # PostgreSQL Configuration
    # ==========================================
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "legal_rag")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_SSLMODE = os.getenv("DB_SSLMODE")
    DB_SSLROOTCERT = os.getenv("DB_SSLROOTCERT")
    DB_SSLCERT = os.getenv("DB_SSLCERT")
    DB_SSLKEY = os.getenv("DB_SSLKEY")
    DB_APPLICATION_NAME = os.getenv("DB_APPLICATION_NAME")
    DB_CONNECT_TIMEOUT = os.getenv("DB_CONNECT_TIMEOUT")

    # ==========================================
    # Pinecone Configuration
    # ==========================================
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "legal-rag")
    PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

    # ==========================================
    # Embedding Configuration
    # ==========================================
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5",
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
