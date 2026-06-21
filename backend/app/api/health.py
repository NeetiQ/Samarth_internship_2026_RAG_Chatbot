"""
Health check endpoints
"""

from fastapi import APIRouter

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
        "database": "unknown",
        "vectordb": "unknown",
        "llm": "unknown",
        "cache": "unknown",
    }
    
    # TODO: Implement actual health checks for each service
    
    return {
        "status": "healthy",
        "timestamp": "2024-01-15T10:00:00Z",
        "services": services_status,
    }
