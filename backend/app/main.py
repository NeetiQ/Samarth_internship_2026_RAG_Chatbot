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
import os
from dotenv import load_dotenv

# Load environments from multiple sources before other app imports
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"), override=False)

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1 import api_router
from app.database.session import engine
settings = get_settings()

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

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "project": settings.PROJECT_NAME}

    @app.get("/ready", tags=["System"])
    async def readiness_check():
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                result = await conn.execute(
                    text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
                )
                if not result.fetchone():
                    raise HTTPException(status_code=503, detail="PGVector extension not loaded")
            return {"status": "ready", "project": settings.PROJECT_NAME}
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=503, detail="Database not ready")

    return app

app = create_app()
