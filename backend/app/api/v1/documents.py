from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.document import DocumentResponse, UploadResponse
from app.schemas.processing import ProcessingJobResponse
from app.services.documents.document_service import DocumentService
from app.services.ingestion.ingestion_service import IngestionService
from app.repositories import job_repo
from app.models.all_models import User
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_doc_service(db: AsyncSession = Depends(get_db)):
    return DocumentService(db)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service),
):
    """Team A & B: Upload document and trigger background processing pipeline."""
    result = await doc_service.upload_document(file, user_id=current_user.id)
    
    # Trigger background pipeline
    background_tasks.add_task(IngestionService.process_document_background, result["document_id"])
    
    return result

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service)
):
    """Team A & B: List documents (user-owned + shared)."""
    return await doc_service.list_documents(skip, limit, user_id=current_user.id)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service)
):
    """Get document details (only if owned by current user or shared)."""
    doc = await doc_service.get_user_document(document_id, current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/{document_id}/status", response_model=ProcessingJobResponse)
async def get_processing_status(
    document_id: int,
    current_user: User = Depends(get_current_user),
    doc_service: DocumentService = Depends(get_doc_service),
    db: AsyncSession = Depends(get_db)
):
    """Poll processing status of a document (ownership verified)."""
    doc = await doc_service.get_user_document(document_id, current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    job = await job_repo.get_by_document_id(db, document_id)
    if not job:
        raise HTTPException(status_code=404, detail="Processing job not found")
    return job
