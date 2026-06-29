from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.all_models import ChatSession, ChatMessage, ChatRole
from app.schemas.chunk import RetrievalResult
from app.repositories import chat_session_repo

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from rag_chat.workflows.rag_pipeline import RAGPipeline
from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.citations.citation_formatter import format_citations
from app.services.retrieval.retrieval_service import RetrievalService

class PromptServiceAdapter:
    def build_prompt(self, query, chunks):
        return build_prompt(query, str(chunks))

class CitationServiceAdapter:
    def generate(self, retrieved_data):
        metadata_list = [chunk.metadata for chunk in retrieved_data.get("chunks", []) if getattr(chunk, "metadata", None)]
        return format_citations(metadata_list)
        
class LLMServiceAdapter:
    def generate(self, prompt):
        try:
            from rag_chat.llm.gemini_client import generate_response
            return generate_response(prompt)
        except ValueError as e:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail=f"LLM Configuration Error: {str(e)}")
        except Exception as e:
            raise e

class RetrievalServiceAdapter:
    def __init__(self, backend_retrieval_service: RetrievalService):
        self.retrieval_service = backend_retrieval_service
        
    def retrieve(self, query):
        # Call Team B's synchronous retriever directly since we are already in a thread pool
        # Bypass the async full_retrieve which would otherwise require an event loop
        # Note: self.retrieval_service.retriever is the Team B Retriever instance
        results_dicts = self.retrieval_service.retriever.retrieve(query, top_k=5)
        # Parse into RetrievalResult to match original adapter logic
        from app.schemas.chunk import RetrievalResult
        results = [RetrievalResult(**r) for r in results_dicts]
        return {"chunks": results, "metadata": [r.metadata for r in results if r.metadata]}

class RagService:
    def __init__(self, db: AsyncSession):
        self.db = db
        backend_retrieval = RetrievalService(db)
        
        self.pipeline = RAGPipeline(
            retrieval_service=RetrievalServiceAdapter(backend_retrieval),
            prompt_service=PromptServiceAdapter(),
            llm_service=LLMServiceAdapter(),
            citation_service=CitationServiceAdapter()
        )

    async def rewrite_query(self, query: str, history: List[ChatMessage]) -> str:
        # Team C didn't implement rewrite explicitly, return query
        return query

    async def generate_response(self, query: str, context: List[RetrievalResult], history: List[ChatMessage]) -> ChatMessage:
        import asyncio
        loop = asyncio.get_event_loop()
        # Team C's pipeline is sync
        result = await loop.run_in_executor(None, self.pipeline.process_query, query)
        
        msg = ChatMessage(role=ChatRole.ASSISTANT, content=result["answer"])
        return msg

    async def get_session(self, session_id: int) -> Optional[ChatSession]:
        return await chat_session_repo.get(self.db, id=session_id)

    async def get_history(self, session_id: int) -> List[ChatMessage]:
        session = await self.get_session(session_id)
        if session:
            return session.messages
        return []
