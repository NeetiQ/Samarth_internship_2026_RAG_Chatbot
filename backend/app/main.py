from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
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

# Load environments from multiple sources before other app imports
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"), override=False)

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
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
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Legal RAG System Backend Foundation",
        version="1.0.0",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    async def log_deployment_info():
        """Log deployment configuration on startup (never logs passwords)."""
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
            logger.info(f"  Environment : {settings.ENVIRONMENT}")
            logger.info(f"  DB Host     : {db_host}:{db_port}")
            logger.info(f"  DB Name     : {db_name}")
            logger.info(f"  DB Provider : {provider}")
            logger.info(f"  SSL Enabled : {ssl_enabled}")
            logger.info(f"  Debug Mode  : {settings.DEBUG}")
            logger.info("=" * 60)
        except Exception as e:
            logger.warning(f"Could not log deployment info: {e}")

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "project": settings.PROJECT_NAME}

    @app.get("/ready", tags=["System"])
    async def readiness_check():
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                # Removed PGVector check. Pinecone is now used for vector storage.
            return {"status": "ready", "project": settings.PROJECT_NAME}
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=503, detail="Database not ready")

    return app

app = create_app()

