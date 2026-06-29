from app.repositories.base_repository import BaseRepository
from app.models.all_models import Document

class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)

document_repo = DocumentRepository()
