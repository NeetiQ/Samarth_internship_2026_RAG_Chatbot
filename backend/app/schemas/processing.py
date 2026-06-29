from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.all_models import ProcessingStage

class ProcessingJobBase(BaseModel):
    document_id: int
    stage: ProcessingStage
    status: str
    error_message: Optional[str] = None

class ProcessingJobResponse(ProcessingJobBase):
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
