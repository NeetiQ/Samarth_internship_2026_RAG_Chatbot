from app.repositories.base_repository import BaseRepository
from app.models.all_models import ChatSession

class ChatSessionRepository(BaseRepository[ChatSession]):
    def __init__(self):
        super().__init__(ChatSession)

chat_session_repo = ChatSessionRepository()
