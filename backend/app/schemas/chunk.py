from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

class ChunkBase(BaseModel):
    document_id: int
    content: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    paragraph: Optional[int] = None
    chunk_index: int

class ChunkCreate(ChunkBase):
    pass

class ChunkResponse(ChunkBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    document_ids: Optional[List[int]] = None
    
class RetrievalResult(BaseModel):
    chunk_id: str
    page_content: str
    metadata: Optional[Dict[str, Any]] = None
    score: float
    
class RetrievalResponse(BaseModel):
    query: str
    results: List[RetrievalResult]
