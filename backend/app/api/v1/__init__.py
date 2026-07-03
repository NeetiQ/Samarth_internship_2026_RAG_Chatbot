from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router
from app.api.v1.extraction import router as extraction_router
from app.api.v1.retrieval import router as retrieval_router
from app.api.v1.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(documents_router, prefix="/documents", tags=["Documents"])
api_router.include_router(extraction_router, prefix="/extraction", tags=["Extraction"])
api_router.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
