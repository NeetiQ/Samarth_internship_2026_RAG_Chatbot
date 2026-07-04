# Backend Endpoints

Interactive Swagger UI is available at `/api/v1/docs`.

## Documents & Ingestion (Teams A & E)
- `POST /api/v1/documents/upload`: Upload a file and trigger background processing.
- `GET /api/v1/documents`: List all uploaded documents.
- `GET /api/v1/documents/{document_id}`: Get document details and structured metadata.
- `GET /api/v1/documents/{document_id}/status`: Poll the processing job stage.

## Extraction overrides (Team A)
- `POST /api/v1/extraction/process/{document_id}`: Manually re-trigger the ingestion pipeline.

## Retrieval (Team B)
- `POST /api/v1/retrieval/retrieve`: Perform a similarity search over chunks. Expects `query` and `top_k`.

## Chat & LLM (Team C)
- `POST /api/v1/chat`: Send a message to Gemini. If `use_rag=true`, it will fetch context from Retrieval.
- `POST /api/v1/chat/history`: Create a new session.
- `GET /api/v1/chat/history/{session_id}`: Retrieve past messages.
- `POST /api/v1/chat/query-rewrite`: Rewrite the query based on history before searching.

## System
- `GET /api/v1/health`: Basic health and config check.
