from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException
from typing import List, Optional
from app.repositories import document_repo, job_repo
from app.services.storage.storage_service import StorageService
from app.models.all_models import Document, ProcessingStage

class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_service = StorageService()

    async def upload_document(self, file: UploadFile) -> dict:
        if not self.storage_service.validate_file_type(file.content_type):
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        file_path = await self.storage_service.save_file(file)
        
        # Save to DB via repo
        doc = await document_repo.create(self.db, obj_in={
            "title": file.filename,
            "filename": file.filename,
            "file_type": file.content_type,
            "file_path": file_path
        })
        
        # Create processing job
        job = await job_repo.create(self.db, obj_in={
            "document_id": doc.id,
            "stage": ProcessingStage.UPLOADED,
            "status": "completed"
        })
        
        return {"document_id": doc.id, "job_id": job.id, "status": "uploaded"}

    async def get_document(self, document_id: int) -> Optional[Document]:
        return await document_repo.get(self.db, id=document_id)

    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        return await document_repo.get_multi(self.db, skip=skip, limit=limit)
