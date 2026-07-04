"""
Chat API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import logging

from rag_chat.workflows.rag_pipeline import process_query

logger = logging.getLogger(__name__)

router = APIRouter()

# TODO: Add chat endpoints


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: str
    session_id: Optional[str] = None
    stream: bool = False


class Citation(BaseModel):
    """Citation model for response."""
    text: str
    source: str
    page: int
    chunk_id: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    id: str
    content: str
    citations: List[Citation] = []
    metadata: dict = {}


@router.post("", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message and get a response from the RAG system.
    
    Args:
        request: Chat request containing message and conversation context
    
    Returns:
        Chat response with generated content and citations
    """
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message content cannot be empty"
        )
    
    start_time = time.time()
    try:
        result = process_query(request.message, history=None)
        
        citations = []
        for c in result.get("citations", []):
            citations.append(Citation(
                text=c.get("text", ""),
                source=c.get("source", "Unknown"),
                page=c.get("page", 0),
                chunk_id=str(c.get("chunk_id", ""))
            ))
            
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            id=f"msg_{int(time.time())}",
            content=result.get("answer", ""),
            citations=citations,
            metadata={
                "processing_time_ms": processing_time_ms,
                "conversation_id": request.conversation_id
            }
        )
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
