from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from app.models.all_models import ChatSession, ChatMessage, ChatRole
from app.schemas.chunk import RetrievalResult
from app.schemas.chat import CitationResponse
from app.repositories import chat_session_repo

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.citations.citation_formatter import format_citations
from rag_chat.llm.gemini_client import generate_response as gemini_generate
from app.services.retrieval.retrieval_service import RetrievalService
from fastapi import HTTPException

class RagService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.retrieval_service = RetrievalService(db)

    async def rewrite_query(self, query: str, history: List[ChatMessage]) -> str:
        # Team C didn't implement rewrite explicitly, return query
        return query

    async def generate_response(self, query: str, context: List[RetrievalResult], history: List[ChatMessage]) -> Tuple[ChatMessage, List[CitationResponse]]:
        import asyncio
        loop = asyncio.get_event_loop()
        
        def run_pipeline():
            # 1. Retrieve
            results_dicts = self.retrieval_service.retriever.retrieve(query, top_k=5)
            chunks_text = "\n".join([r.get("page_content", "") for r in results_dicts])
            citations = [
                CitationResponse(
                    chunk_id=r.get("chunk_id"),
                    score=r.get("score"),
                    content=r.get("page_content"),
                    document_id=(r.get("metadata") or {}).get("doc_id"),
                )
                for r in results_dicts
            ]
            
            # 2. Build Prompt
            prompt = build_prompt(question=query, context=chunks_text, history=history)
            
            # 3. Generate Answer
            try:
                answer = gemini_generate(prompt)
            except ValueError as e:
                raise HTTPException(status_code=503, detail=f"LLM Configuration Error: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"Gemini unavailable: {str(e)}")
            return answer, citations
            
        answer, citations = await loop.run_in_executor(None, run_pipeline)
        
        msg = ChatMessage(role=ChatRole.ASSISTANT, content=answer)
        return msg, citations

    async def get_session(self, session_id: int) -> Optional[ChatSession]:
        return await chat_session_repo.get(self.db, id=session_id)

    async def get_history(self, session_id: int) -> List[ChatMessage]:
        session = await self.get_session(session_id)
        if session:
            return session.messages
        return []
