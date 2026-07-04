from app.repositories.base_repository import BaseRepository
from app.models.all_models import ChatSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

class ChatSessionRepository(BaseRepository[ChatSession]):
    def __init__(self):
        super().__init__(ChatSession)

    async def get_multi_by_user(
        self, db: AsyncSession, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[ChatSession]:
        """Return chat sessions belonging to the given user."""
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_user_session(
        self, db: AsyncSession, session_id: int, user_id: int
    ) -> Optional[ChatSession]:
        """Get a chat session only if the user owns it."""
        query = select(self.model).where(
            self.model.id == session_id,
            self.model.user_id == user_id,
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

chat_session_repo = ChatSessionRepository()
