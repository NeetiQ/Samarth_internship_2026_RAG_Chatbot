"""
Entry point for the Retrieval Service API.
"""

from fastapi import FastAPI

from retrieval.api.routes import router

app = FastAPI(
    title="Retrieval Service API",
    description="Semantic Retrieval API for Legal RAG Chatbot",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Retrieval Service is running."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}