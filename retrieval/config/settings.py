import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    # PostgreSQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "legal_rag")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Embedding Model
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5"
    )

    # Retrieval
    TOP_K = int(os.getenv("TOP_K", 5))
    SIMILARITY = os.getenv("SIMILARITY", "cosine")