from app.repositories.base_repository import BaseRepository
from app.models.all_models import Chunk
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

class ChunkRepository(BaseRepository[Chunk]):
    def __init__(self):
        super().__init__(Chunk)

    async def get_by_document_id(self, db: AsyncSession, document_id: int) -> List[Chunk]:
        query = select(self.model).where(self.model.document_id == document_id)
        result = await db.execute(query)
        return list(result.scalars().all())

chunk_repo = ChunkRepository()
