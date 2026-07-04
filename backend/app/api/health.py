"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime
import psycopg2

router = APIRouter()


@router.get("")
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        Health status of the application
    """
    return {
        "status": "healthy",
        "service": "legal-rag-backend",
        "version": "0.1.0",
    }


@router.get("/detailed")
async def detailed_health_check():
    """
    Detailed health check including all service dependencies.
    
    Returns:
        Detailed health status including database, vector DB, LLM, etc.
    """
    services_status = {
        "database": "unhealthy",
        "vectordb": "unhealthy",
        "llm": "unknown",
        "cache": "unknown",
    }
    
    from app.core.settings import get_settings
    settings = get_settings()
    # Use the centralized, validated DATABASE_URL from settings.
    # Rewrite the asyncpg dialect to the synchronous postgresql dialect
    # that psycopg2 expects.
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql+asyncpg"):
        db_url = db_url.replace("postgresql+asyncpg", "postgresql", 1)
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        services_status["database"] = "healthy"
        
        # Pinecone vector database check
        try:
            from pinecone import Pinecone
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            pc.describe_index(settings.PINECONE_INDEX_NAME)
            services_status["vectordb"] = "healthy"
        except Exception as e:
            services_status["vectordb"] = f"unhealthy: {str(e)}"
        
        cur.close()
        conn.close()
    except Exception:
        pass
    
    overall_status = "healthy" if services_status["database"] == "healthy" and services_status["vectordb"] == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "services": services_status,
    }
