from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.chunk import ChunkResponse
from app.services.ingestion.ingestion_service import IngestionService
from app.services.documents.document_service import DocumentService
from app.models.all_models import User
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_ingestion_service(db: AsyncSession = Depends(get_db)):
    return IngestionService(db)

def get_doc_service(db: AsyncSession = Depends(get_db)):
    return DocumentService(db)

@router.post("/process/{document_id}", response_model=MessageResponse)
async def trigger_reprocess(
    document_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service),
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    """Team A: Manually re-trigger processing pipeline for a document (ownership verified)."""
    doc = await doc_service.get_user_document(document_id, current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    background_tasks.add_task(ingestion_service.process_document_background, document_id)
    return {"message": "Processing pipeline initiated"}

@router.get("/chunks/{document_id}", response_model=List[ChunkResponse])
async def get_document_chunks(
    document_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service),
    db: AsyncSession = Depends(get_db)
):
    """Team A: Get chunks for a document (ownership verified)."""
    from app.repositories import chunk_repo
    
    doc = await doc_service.get_user_document(document_id, current_user.id)
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
