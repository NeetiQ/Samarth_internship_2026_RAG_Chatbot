from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

from app.core.settings import get_settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler,
)

import logging
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load root .env before importing anything that depends on environment variables
load_dotenv(
    os.path.join(os.path.dirname(__file__), "../../.env"),
    override=True,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.api.v1 import api_router
from app.database.session import engine

settings = get_settings()

logger = logging.getLogger("legal-rag")


def _detect_provider(hostname: str) -> str:
    """Detect cloud database provider from the hostname."""
    provider_hints = {
        "render.com": "Render",
        "neon.tech": "Neon",
        "supabase.co": "Supabase",
        "amazonaws.com": "AWS RDS",
        "azure.com": "Azure",
        "cloudsql": "Google Cloud SQL",
        "elephantsql.com": "ElephantSQL",
        "aiven.io": "Aiven",
    }

    for hint, name in provider_hints.items():
        if hint in hostname:
            return name

    if hostname in ("localhost", "127.0.0.1", "db"):
        return "Local / Docker"

    return "Unknown"


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            parsed = urlparse(settings.DATABASE_URL)
            db_host = parsed.hostname or "unknown"
            db_port = parsed.port or 5432
            db_name = (parsed.path or "").lstrip("/") or "unknown"
            ssl_enabled = "sslmode" in (parsed.query or "")
            provider = _detect_provider(db_host)

            logger.info("=" * 60)
            logger.info("DEPLOYMENT CONFIGURATION")
            logger.info("=" * 60)
            logger.info(f"Environment : {settings.ENVIRONMENT}")
            logger.info(f"DB Host     : {db_host}:{db_port}")
            logger.info(f"DB Name     : {db_name}")
            logger.info(f"DB Provider : {provider}")
            logger.info(f"SSL Enabled : {ssl_enabled}")
            logger.info(f"Debug Mode  : {settings.DEBUG}")
            logger.info("=" * 60)

        except Exception as e:
            logger.warning(f"Could not log deployment info: {e}")
        yield

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Legal RAG System Backend Foundation",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:8000",
            "http://localhost",
            "https://samarth-internship-2026-rag-chatbot.vercel.app",
            "https://samarth-internship-2026-rag-chatbot-dgxzw5len.vercel.app"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        SQLAlchemyError,
        sqlalchemy_exception_handler,
    )
    app.add_exception_handler(
        Exception,
        general_exception_handler,
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)



    @app.get("/health", tags=["System"])
    async def health_check():
        return {
            "status": "ok",
            "project": settings.PROJECT_NAME,
        }

    @app.get("/ready", tags=["System"])
    async def readiness_check():
        from app.services.vector.pinecone_service import PineconeService
        from retrieval.embeddings.client import EmbeddingClient

        errors = {}

        # 1. PostgreSQL check
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            errors["database"] = f"Database check failed: {str(e)}"

        # 2. Pinecone check
        try:
            if not PineconeService.check_health():
                errors["pinecone"] = "Pinecone index status check failed."
        except Exception as e:
            errors["pinecone"] = f"Pinecone connection failed: {str(e)}"

        # 3. Embedding Service check
        try:
            client = EmbeddingClient()
            health_status = client.get_health()
            if health_status.get("status") != "healthy":
                errors["embedding_service"] = f"Embedding Service status: {health_status.get('status')}"
        except Exception as e:
            errors["embedding_service"] = f"Embedding Service connection failed: {str(e)}"

        if errors:
            raise HTTPException(
                status_code=503,
                detail={"message": "System not ready", "components": errors}
            )

        return {
            "status": "ready",
            "project": settings.PROJECT_NAME,
            "components": {
                "database": "healthy",
                "pinecone": "healthy",
                "embedding_service": "healthy"
            }
        }

    return app


app = create_app()