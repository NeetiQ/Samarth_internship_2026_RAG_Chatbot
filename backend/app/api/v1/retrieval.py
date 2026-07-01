from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.chunk import RetrievalRequest, RetrievalResponse
from app.services.retrieval.retrieval_service import RetrievalService
from app.models.all_models import User
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_retrieval_service(db: AsyncSession = Depends(get_db)):
    return RetrievalService(db)

@router.post("/retrieve", response_model=RetrievalResponse)
async def retrieve_chunks(
    request: RetrievalRequest,
    current_user: User = Depends(get_current_user),
    ret_service: RetrievalService = Depends(get_retrieval_service)
):
    """Team B: Retrieve and rerank chunks (shared corpus, auth required)."""
    results = await ret_service.full_retrieve(request.query, top_k=request.top_k)
    return RetrievalResponse(query=request.query, results=results)
