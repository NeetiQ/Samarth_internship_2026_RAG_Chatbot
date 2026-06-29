import os
from fastapi import UploadFile
from app.core.settings import get_settings

settings = get_settings()

class StorageService:
    def __init__(self):
        self.storage_dir = settings.STORAGE_DIR
        os.makedirs(self.storage_dir, exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        file_path = os.path.join(self.storage_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return file_path

    async def delete_file(self, file_path: str) -> bool:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
        
    def validate_file_type(self, content_type: str) -> bool:
        return content_type in settings.SUPPORTED_FILE_TYPES
