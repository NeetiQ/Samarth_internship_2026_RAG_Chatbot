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
from app.models.all_models import User
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_rag_service(db: AsyncSession = Depends(get_db)):
    return RagService(db)

from app.repositories import chat_session_repo
from app.models.all_models import ChatSession

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Main chat endpoint with RAG context."""
    from app.core.diagnostic_logger import Profiler
    
    with Profiler("Entering chat endpoint POST /api/v1/chat"):
        # If session_id provided, verify ownership
        if request.session_id:
            with Profiler("Chat session lookup"):
                session = await chat_session_repo.get_user_session(
                    rag_service.db, request.session_id, current_user.id
                )
            if not session:
                raise HTTPException(status_code=403, detail="Chat session not found or access denied")
        
        # Simplified context & history gathering for integration
        with Profiler("Chat history lookup"):
            history = await rag_service.get_history(request.session_id) if request.session_id else []
        context = [] # Let pipeline handle retrieval directly!
        
        try:
            with Profiler("rag_service.generate_response"):
                response_msg, citations = await rag_service.generate_response(request.message, context, history)
        except HTTPException:
            raise
        except ValueError as e:
            if "GEMINI_API_KEY" in str(e):
                raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured or invalid.")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            import logging
            logging.getLogger("legal-rag-diagnostics").exception("Fatal exception in generate_response")
            if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
                 raise HTTPException(status_code=503, detail="GEMINI_API_KEY not configured or invalid.")
            raise HTTPException(status_code=500, detail=str(e))
        
        with Profiler("Returning HTTP response"):
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Team C: Create a new chat session (owned by current user)."""
    session = await chat_session_repo.create(db, obj_in={
        "title": "New Session",
        "user_id": current_user.id,
    })
    return ChatSessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.get("/history/{session_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Get chat history (ownership verified)."""
    session = await chat_session_repo.get_user_session(
        rag_service.db, session_id, current_user.id
    )
    if not session:
        raise HTTPException(status_code=403, detail="Chat session not found or access denied")
    return await rag_service.get_history(session_id)

@router.delete("/history/{session_id}", response_model=MessageResponse)
async def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Team C: Delete a session (ownership verified)."""
    session = await chat_session_repo.get_user_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(status_code=403, detail="Chat session not found or access denied")
    await chat_session_repo.remove(db, id=session_id)
    return MessageResponse(message="Session deleted successfully")

@router.post("/query-rewrite", response_model=QueryRewriteResponse)
async def rewrite_query(
    request: QueryRewriteRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RagService = Depends(get_rag_service)
):
    """Team C: Rewrite user query using history."""
    result = await rag_service.rewrite_query(request.query, request.history)
    return QueryRewriteResponse(rewritten_query=result)
