"""
FastAPI Backend Application
"""

from fastapi import FastAPI

app = FastAPI(
    title="Legal RAG API",
    description="Retrieval Augmented Generation for Legal Documents",
    version="0.1.0",
)
        "application": "Legal RAG",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
