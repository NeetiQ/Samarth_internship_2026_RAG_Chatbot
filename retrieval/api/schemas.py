"""
Pydantic request and response schemas.
"""

from typing import Any

from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    """Request schema for semantic retrieval."""

    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResponse(BaseModel):
    """Response schema for retrieved chunks."""

    chunk_id: str
    page_content: str
    metadata: dict[str, Any]
    score: float


class IndexRequest(BaseModel):
    """Request schema for document indexing."""

    jsonl_path: str