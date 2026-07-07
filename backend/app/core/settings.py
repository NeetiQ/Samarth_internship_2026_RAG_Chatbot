from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legal RAG API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    
    # Database URL has no default; it is required.
    DATABASE_URL: str
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        if not v:
            raise ValueError("DATABASE_URL environment variable is missing. A valid database connection string is required.")
        
        import builtins
        def mask_url(url_str: str) -> str:
            if not url_str: return ""
            try:
                import urllib.parse
                parsed = urllib.parse.urlparse(url_str)
                if parsed.password:
                    return url_str.replace(parsed.password, "******")
            except: pass
            return url_str

        builtins.print(f"validate_database_url: Input URL = {mask_url(v)}", flush=True)

        env = info.data.get("ENVIRONMENT", "production")
        if env == "production":
            if "localhost" in v or "127.0.0.1" in v:
                raise ValueError("Production environment should never connect to localhost.")
            if "postgres:postgres@" in v:
                raise ValueError("Production environment should never use default development credentials.")
        
        # Cloud providers often inject postgres:// or postgresql:// natively. 
        # We rewrite it to the asyncpg dialect required by SQLAlchemy.
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        if "sslmode=require" in v:
            v = v.replace("sslmode=require", "ssl=true")
        elif "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=")
        if "channel_binding=" in v:
            v = v.replace("&channel_binding=require", "")
            v = v.replace("?channel_binding=require&", "?")
            v = v.replace("?channel_binding=require", "")
            
        builtins.print(f"validate_database_url: Output URL = {mask_url(v)}", flush=True)
        return v
    
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
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384
    RETRIEVAL_TOP_K: int = 5
    RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    RERANKER_TOP_K: int = 3
    EMBEDDING_SERVICE_URL: str = "http://localhost:7860"
    EMBEDDING_SERVICE_API_KEY: str = ""
    
    # Pinecone Vector DB
    PINECONE_API_KEY: str
    PINECONE_INDEX: str
    PINECONE_NAMESPACE: str = "default"
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"
    
    @field_validator("PINECONE_API_KEY", mode="before")
    @classmethod
    def validate_pinecone_api_key(cls, v: Optional[str]) -> str:
        if not v:
            raise ValueError("PINECONE_API_KEY environment variable is required.")
        return v
    
    # LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Corpus seeding (deployment)
    SEED_CORPUS: bool = True
    CHUNKED_DOCUMENTS_PATH: str = "./chunked_documents.jsonl"
    EMBEDDED_DOCUMENTS_PATH: str = "./embedded_documents.jsonl"
    GENERATE_EMBEDDINGS_ON_SEED: bool = False
    
    # JWT / Auth
    SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")


import builtins
@lru_cache
def get_settings():
    builtins.print("get_settings: Instantiating Settings()", flush=True)
    s = Settings()
    builtins.print("get_settings: Settings instantiated", flush=True)
    return s
