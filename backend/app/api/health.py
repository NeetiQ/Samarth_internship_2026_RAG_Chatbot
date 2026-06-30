"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime
import psycopg2
import os

router = APIRouter()

# TODO: Add health check endpoints


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
    
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgresql+asyncpg"):
        db_url = db_url.replace("postgresql+asyncpg", "postgresql")
    
    try:
        if db_url:
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            cur.execute("SELECT 1")
            services_status["database"] = "healthy"
            
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            if cur.fetchone():
                services_status["vectordb"] = "healthy"
            
            cur.close()
            conn.close()
    except Exception as e:
        pass
    
    overall_status = "healthy" if services_status["database"] == "healthy" and services_status["vectordb"] == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "services": services_status,
    }
