from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.all_models import ProcessingStage

class DocumentBase(BaseModel):
    title: str
    filename: str
    file_type: Optional[str] = None
    court: Optional[str] = None
    case_number: Optional[str] = None
    judgment_date: Optional[datetime] = None
    source: Optional[str] = None
    language: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    court: Optional[str] = None
    case_number: Optional[str] = None
    judgment_date: Optional[datetime] = None
    source: Optional[str] = None
    language: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UploadResponse(BaseModel):
    document_id: int
    job_id: int
    status: str
