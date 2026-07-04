"""
Configuration management
"""

from pydantic_settings import BaseSettings

# TODO: Add configuration settings here
    
    # Application
    app_name: str = "Legal RAG"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/legal_rag"
    )
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    
    # Vector Database
    vectordb_type: str = os.getenv("VECTORDB_TYPE", "pinecone")
    vectordb_url: str = os.getenv("VECTORDB_URL", "")
    vectordb_api_key: str = os.getenv("VECTORDB_API_KEY", "")
    vectordb_index_name: str = os.getenv("VECTORDB_INDEX_NAME", "legal-rag")
    
    # LLM Configuration
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    # Embeddings
    embeddings_provider: str = os.getenv("EMBEDDINGS_PROVIDER", "openai")
    embeddings_model: str = os.getenv(
        "EMBEDDINGS_MODEL",
        "text-embedding-3-small"
    )
    embeddings_dimension: int = int(os.getenv("EMBEDDINGS_DIMENSION", "1536"))
    
    # Document Processing
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    allowed_file_types: List[str] = ["pdf", "txt", "doc", "docx"]
    
    # Chunking
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Search
    top_k_results: int = int(os.getenv("TOP_K_SEARCH_RESULTS", "5"))
    reranker_enabled: bool = (
        os.getenv("RERANKER_ENABLED", "true").lower() == "true"
    )
    reranker_model: str = os.getenv(
        "RERANKER_MODEL",
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")
    
    # Session
    session_secret: str = os.getenv(
        "SESSION_SECRET",
        "your-secret-key-change-in-production"
    )
    session_timeout: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
