"""
Retrieval API endpoints
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
import time
import logging

from retrieval.search.retriever import Retriever

logger = logging.getLogger(__name__)

router = APIRouter()
retriever = Retriever()

# TODO: Add retrieval endpoints


class SearchResult(BaseModel):
    """Model for individual search result."""
    id: str
    text: str
    score: float
    document_name: str
    page: int


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    results: List[SearchResult] = []
    total_results: int
    processing_time_ms: int


@router.get("/search", response_model=SearchResponse)
async def search_documents(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20, description="Number of top results"),
    document_id: Optional[str] = Query(None, description="Filter by document"),
):
    """
    Search documents using semantic and hybrid search.
    
    Args:
        q: Search query
        top_k: Number of top results to return
        document_id: Optional document ID to filter results
    
    Returns:
        Search results with relevance scores
    """
    start_time = time.time()
    try:
        raw_results = retriever.retrieve(query=q, top_k=top_k)
        
        results = []
        for r in raw_results:
            results.append(SearchResult(
                id=str(r.get("chunk_id", "")),
                text=r.get("page_content", ""),
                score=float(r.get("distance", 0.0)),
                document_name=r.get("metadata", {}).get("source", "unknown"),
                page=r.get("metadata", {}).get("page", 0)
            ))
            
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return SearchResponse(
            query=q,
            results=results,
            total_results=len(results),
            processing_time_ms=processing_time_ms,
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return SearchResponse(
            query=q,
            results=[],
            total_results=0,
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
