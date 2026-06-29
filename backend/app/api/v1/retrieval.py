from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.chunk import RetrievalRequest, RetrievalResponse
from app.services.retrieval.retrieval_service import RetrievalService

router = APIRouter()

def get_retrieval_service(db: AsyncSession = Depends(get_db)):
    return RetrievalService(db)

@router.post("/retrieve", response_model=RetrievalResponse)
async def retrieve_chunks(
    request: RetrievalRequest,
    ret_service: RetrievalService = Depends(get_retrieval_service)
):
    """Team B: Retrieve and rerank chunks."""
    results = await ret_service.full_retrieve(request.query, top_k=request.top_k)
    return RetrievalResponse(query=request.query, results=results)
