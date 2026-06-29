# Legal RAG Backend Foundation (V2)

Production-ready backend architecture for the Legal Retrieval-Augmented Generation (RAG) assistant.

## Features
- **Clean Architecture**: Domain-driven services, Repositories, and modular Routers.
- **Asynchronous**: FastAPI async routers, `asyncpg` for PostgreSQL.
- **PGVector Native**: Embeddings are stored natively in the `chunks` table.
- **Background Processing**: `ProcessingJob` model tracks ingestion pipelines without heavy queues like Celery.

## Quick Start (Docker)

Ensure Docker and Docker Compose are installed. 

```bash
docker-compose up --build
```
This starts:
1. `db`: PostgreSQL 16 with `pgvector` enabled.
2. `api`: The FastAPI server on port `8000`.

View Swagger Docs at: `http://localhost:8000/docs`

## Configuration
All configurable values (Chunk sizes, OCR engine, Model names, etc.) are loaded via `pydantic-settings` from the `.env` file or environment variables. Do not hardcode these in the application logic. Modify `app/core/settings.py` for new keys.

## Folder Structure
- `app/api/v1/`: HTTP Routers. **No business logic here.**
- `app/services/`: Domain-specific business logic (documents, storage, ingestion, retrieval, rag, shared).
- `app/repositories/`: Database abstraction layer (SQLAlchemy wrappers).
- `app/models/`: SQLAlchemy declarative tables.
- `app/schemas/`: Pydantic validation for API I/O.
- `docs/`: API Contracts, DB schema details.

## How to Extend (For Teams)
- **Team A (Ingestion)**: Implement logic in `app/services/ingestion/ingestion_service.py` (`process_document_background`).
- **Team B (Retrieval)**: Implement PGVector queries in `app/services/retrieval/retrieval_service.py`.
- **Team C (LLM)**: Implement Gemini orchestration in `app/services/rag/rag_service.py`.

*Note: You do not need to modify routers or repositories unless you are altering the DB schema or adding brand new endpoints.*
