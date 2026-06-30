from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from app.database.session import get_db
from app.schemas.chat import (
    ChatRequest, ChatResponse, ChatSessionResponse, 
    ChatMessageResponse, QueryRewriteRequest, QueryRewriteResponse
)
from app.schemas.common import MessageResponse
from app.services.rag.rag_service import RagService

router = APIRouter()

def get_rag_service(db: AsyncSession = Depends(get_db)):
    return RagService(db)

from app.repositories import chat_session_repo
from app.models.all_models import ChatSession

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Main chat endpoint with RAG context."""
    # Simplified context & history gathering for integration
    history = await rag_service.get_history(request.session_id) if request.session_id else []
    context = [] # Let pipeline handle retrieval directly!
    
    try:
        response_msg, citations = await rag_service.generate_response(request.message, context, history)
    except HTTPException:
        raise
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured or invalid.")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
             raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured or invalid.")
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return formatted response
    return ChatResponse(
        session_id=request.session_id or 0,
        message=ChatMessageResponse(
            id=0,
            session_id=request.session_id or 0,
            role=response_msg.role,
            content=response_msg.content,
            created_at=response_msg.created_at or datetime.utcnow(),
            citations=citations
        )
    )

@router.post("/history", response_model=ChatSessionResponse)
async def create_chat_session(
    db: AsyncSession = Depends(get_db)
):
    """Team C: Create a new chat session."""
    session = await chat_session_repo.create(db, obj_in={"title": "New Session"})
    return ChatSessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.get("/history/{session_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(
    session_id: int,
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Get chat history."""
    return await rag_service.get_history(session_id)

@router.delete("/history/{session_id}", response_model=MessageResponse)
async def delete_chat_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Team C: Delete a session."""
    await chat_session_repo.remove(db, id=session_id)
    return MessageResponse(message="Session deleted successfully")

@router.post("/query-rewrite", response_model=QueryRewriteResponse)
async def rewrite_query(
    request: QueryRewriteRequest,
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Rewrite user query using history."""
    result = await rag_service.rewrite_query(request.query, request.history)
    return QueryRewriteResponse(rewritten_query=result)
