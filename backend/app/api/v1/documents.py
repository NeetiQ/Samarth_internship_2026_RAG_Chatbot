from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.document import DocumentResponse, UploadResponse
from app.schemas.processing import ProcessingJobResponse
from app.services.documents.document_service import DocumentService
from app.services.ingestion.ingestion_service import IngestionService
from app.repositories import job_repo

router = APIRouter()

def get_doc_service(db: AsyncSession = Depends(get_db)):
    return DocumentService(db)

def get_ingestion_service(db: AsyncSession = Depends(get_db)):
    return IngestionService(db)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    doc_service: DocumentService = Depends(get_doc_service),
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    """Team A & B: Upload document and trigger background processing pipeline."""
    result = await doc_service.upload_document(file)
    
    # Trigger background pipeline
    background_tasks.add_task(ingestion_service.process_document_background, result["document_id"])
    
    return result

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0, limit: int = 100,
    doc_service: DocumentService = Depends(get_doc_service)
):
    """Team A & B: List documents."""
    return await doc_service.list_documents(skip, limit)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    doc_service: DocumentService = Depends(get_doc_service)
):
    """Get document details."""
    doc = await doc_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/{document_id}/status", response_model=ProcessingJobResponse)
async def get_processing_status(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Poll processing status of a document."""
    job = await job_repo.get_by_document_id(db, document_id)
    if not job:
        raise HTTPException(status_code=404, detail="Processing job not found")
    return job
