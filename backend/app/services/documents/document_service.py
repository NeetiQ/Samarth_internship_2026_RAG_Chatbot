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

    async def upload_document(self, file: UploadFile, user_id: int) -> dict:
        if not self.storage_service.validate_file_type(file.content_type):
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        file_path = await self.storage_service.save_file(file)
        
        # Save to DB via repo — assign ownership to the authenticated user
        doc = await document_repo.create(self.db, obj_in={
            "title": file.filename,
            "filename": file.filename,
            "file_type": file.content_type,
            "file_path": file_path,
            "user_id": user_id,
            "is_shared": False,
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

    async def get_user_document(self, document_id: int, user_id: int) -> Optional[Document]:
        """Get a document only if the user owns it or it is shared."""
        return await document_repo.get_user_document(self.db, document_id, user_id)

    async def list_documents(self, skip: int = 0, limit: int = 100, user_id: int = None) -> List[Document]:
        if user_id is not None:
            return await document_repo.get_multi_by_user(self.db, user_id, skip=skip, limit=limit)
        return await document_repo.get_multi(self.db, skip=skip, limit=limit)
