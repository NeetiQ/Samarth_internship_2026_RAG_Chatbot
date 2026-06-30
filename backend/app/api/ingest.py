"""
Ingestion API endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import shutil
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# TODO: Add ingestion endpoints


class IngestResponse(BaseModel):
    """Response model for ingest endpoint."""
    job_id: str
    status: str
    filename: str
    estimated_completion: str


@router.post("/upload", response_model=IngestResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a document for ingestion.
    
    Args:
        file: Document file to ingest
    
    Returns:
        Ingestion job details
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File must have a filename"
        )
    
    job_id = str(uuid.uuid4())
    upload_dir = os.path.join("Data", "english")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    logger.info(f"Document upload initiated: {file.filename}")
    
    # We will simulate calling the ingestion pipeline in the background for now,
    # or actually import and call `pipeline.main()` if we configure it correctly.
    # To avoid blocking or complex sys.path issues, we execute the shell command.
    def run_ingestion_pipeline():
        os.system("python pipeline.py --no_resume")
        
    background_tasks.add_task(run_ingestion_pipeline)
    
    return IngestResponse(
        job_id=job_id,
        status="processing",
        filename=file.filename,
        estimated_completion="Processing started"
    )


@router.get("/status/{job_id}")
async def get_ingest_status(job_id: str):
    """
    Get the status of an ingestion job.
    
    Args:
        job_id: ID of the ingestion job
    
    Returns:
        Job status and details
    """
    # TODO: Implement job status tracking
    
    return {
        "job_id": job_id,
        "status": "processing",
        "chunks_created": 0,
        "errors": [],
    }
