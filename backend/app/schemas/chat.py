from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.all_models import ChatRole

class CitationResponse(BaseModel):
    chunk_id: Optional[str] = None
    score: Optional[float] = None
    content: Optional[str] = None
    document_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ChatMessageBase(BaseModel):
    role: ChatRole
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    created_at: datetime
    citations: List[CitationResponse] = []
    model_config = ConfigDict(from_attributes=True)

class ChatSessionBase(BaseModel):
    title: Optional[str] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionResponse(ChatSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatSessionDetailResponse(ChatSessionResponse):
    messages: List[ChatMessageResponse] = []

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    message: str
    use_rag: Optional[bool] = True

class ChatResponse(BaseModel):
    session_id: int
    message: ChatMessageResponse
    
class QueryRewriteRequest(BaseModel):
    query: str
    history: List[ChatMessageBase] = []

class QueryRewriteResponse(BaseModel):
    rewritten_query: str
