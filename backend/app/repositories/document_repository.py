from app.repositories.base_repository import BaseRepository
from app.models.all_models import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional

class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)

    async def get_multi_by_user(
        self, db: AsyncSession, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """Return documents owned by the given user OR marked as shared."""
        query = (
            select(self.model)
            .where(
                or_(
                    self.model.user_id == user_id,
                    self.model.is_shared == True,
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_user_document(
        self, db: AsyncSession, document_id: int, user_id: int
    ) -> Optional[Document]:
        """Get a document only if the user owns it or it is shared."""
        query = select(self.model).where(
            self.model.id == document_id,
            or_(
                self.model.user_id == user_id,
                self.model.is_shared == True,
            ),
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

document_repo = DocumentRepository()
