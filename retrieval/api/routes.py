"""
FastAPI routes for the Retrieval Service.
"""

from fastapi import APIRouter, HTTPException

from retrieval.api.schemas import (
    IndexRequest,
    RetrievalRequest,
)
from retrieval.pipelines.retrieval_service import RetrievalService
from retrieval.search.retriever import Retriever

router = APIRouter(prefix="/api/v1", tags=["Retrieval"])

retriever = Retriever()
retrieval_service = RetrievalService()


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "Retrieval Service",
    }


@router.post("/retrieve")
def retrieve(request: RetrievalRequest):
    """
    Retrieve top-k relevant chunks.
    """

    try:

        results = retriever.retrieve(
            query=request.query,
            top_k=request.top_k,
        )

        return {
            "query": request.query,
            "count": len(results),
            "results": results,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@router.post("/documents/index")
def index_documents(request: IndexRequest):
    """
    Index all chunked documents.
    """

    try:

        retrieval_service.index_documents(
            request.jsonl_path
        )

        return {
            "message": "Documents indexed successfully."
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )