from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legal RAG API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "legal_rag"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/legal_rag"
    
    # Storage
    STORAGE_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    SUPPORTED_FILE_TYPES: List[str] = ["application/pdf", "image/png", "image/jpeg"]
    
    # Ingestion & Chunking
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    OCR_ENGINE: str = "PaddleOCR"
    OCR_LANGUAGE: str = "en"
    
    # Embeddings & Retrieval
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-m3"
    EMBEDDING_DIMENSION: int = 1024
    RETRIEVAL_TOP_K: int = 5
    RERANKER_MODEL_NAME: str = "BAAI/bge-reranker-v2-m3"
    RERANKER_TOP_K: int = 3
    
    # LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
