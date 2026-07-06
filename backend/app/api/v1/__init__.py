import builtins
def _trace(msg):
    builtins.print(msg, flush=True)

_trace("api/v1/__init__.py: Starting imports")
from fastapi import APIRouter
_trace("api/v1/__init__.py: Importing auth_router")
from app.api.v1.auth import router as auth_router
_trace("api/v1/__init__.py: Importing documents_router")
from app.api.v1.documents import router as documents_router
_trace("api/v1/__init__.py: Importing extraction_router")
from app.api.v1.extraction import router as extraction_router
_trace("api/v1/__init__.py: Importing retrieval_router")
from app.api.v1.retrieval import router as retrieval_router
_trace("api/v1/__init__.py: Importing chat_router")
from app.api.v1.chat import router as chat_router

_trace("api/v1/__init__.py: Creating APIRouter")
api_router = APIRouter()
_trace("api/v1/__init__.py: Including routers")
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(documents_router, prefix="/documents", tags=["Documents"])
api_router.include_router(extraction_router, prefix="/extraction", tags=["Extraction"])
api_router.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
_trace("api/v1/__init__.py: Finished")
