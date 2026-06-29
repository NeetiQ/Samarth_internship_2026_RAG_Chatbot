from app.repositories.base_repository import BaseRepository
from app.models.all_models import ProcessingJob
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

class ProcessingJobRepository(BaseRepository[ProcessingJob]):
    def __init__(self):
        super().__init__(ProcessingJob)
        
    async def get_by_document_id(self, db: AsyncSession, document_id: int) -> Optional[ProcessingJob]:
        query = select(self.model).where(self.model.document_id == document_id).order_by(self.model.created_at.desc())
        result = await db.execute(query)
        return result.scalar_one_or_none()

job_repo = ProcessingJobRepository()
