from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.chunk import ChunkResponse
from app.services.ingestion.ingestion_service import IngestionService

router = APIRouter()

def get_ingestion_service(db: AsyncSession = Depends(get_db)):
    return IngestionService(db)

@router.post("/process/{document_id}", response_model=MessageResponse)
async def trigger_reprocess(
    document_id: int,
    background_tasks: BackgroundTasks,
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    """Team A: Manually re-trigger processing pipeline for a document."""
    background_tasks.add_task(ingestion_service.process_document_background, document_id)
    return {"message": "Processing pipeline initiated"}

@router.get("/chunks/{document_id}", response_model=List[ChunkResponse])
async def get_document_chunks(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Team A: Get chunks for a document."""
    from app.repositories import chunk_repo, document_repo
    from fastapi import HTTPException
    
    doc = await document_repo.get(db, id=document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    chunks = await chunk_repo.get_by_document_id(db, document_id)
    
    # Map DB chunks to response schema
    return [
        ChunkResponse(
            id=c.id,
            document_id=c.document_id,
            content=c.page_content,
            chunk_index=idx,
            created_at=c.created_at
        ) for idx, c in enumerate(chunks)
    ]
