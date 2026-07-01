# Legal RAG — Release Candidate 1

A full-stack Legal Retrieval-Augmented Generation (RAG) assistant. Upload legal PDFs, run OCR and chunking, store embeddings in PGVector, retrieve relevant passages, and chat with Gemini-powered answers including citations.

## Features

- **Authentication & Authorization** — JWT-based signup/login with user-scoped documents and chat sessions
- **PDF Upload & OCR** — PaddleOCR extraction with background processing jobs
- **Chunking & Embeddings** — LangChain text splitting with SentenceTransformer (`BAAI/bge-small-en-v1.5`)
- **PGVector Retrieval** — Cosine similarity search with optional reranking
- **Gemini LLM** — Context-aware chat with citation formatting
- **React Frontend** — Dashboard, upload, chat, and case comparison UI

## Architecture

```
┌─────────────┐     JWT      ┌──────────────────┐
│   React     │ ──────────►  │  FastAPI Backend │
│  Frontend   │              │  (backend/app)   │
└─────────────┘              └────────┬─────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
              ┌──────────┐    ┌────────────┐    ┌────────────┐
              │PostgreSQL│    │  Team A    │    │  Team C    │
              │ PGVector │    │ Ingestion  │    │ RAG/Gemini │
              └──────────┘    └────────────┘    └────────────┘
```

### RAG Pipeline

1. **Upload** — PDF stored via `DocumentService`, processing job queued
2. **Extract** — `pdf_extractor` + PaddleOCR (`IngestionService`)
3. **Chunk** — `DocumentChunker` splits cleaned text
4. **Embed** — `Embedder` generates vectors, stored in `chunks` table
5. **Retrieve** — `Retriever` queries PGVector on user query
6. **Generate** — `RagService` builds prompt, calls Gemini, returns citations

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI, SQLAlchemy (async), Alembic |
| Database | PostgreSQL 16 + pgvector |
| Embeddings | sentence-transformers, PyTorch |
| LLM | Google Gemini (`google-genai`) |
| OCR | PaddleOCR, PyMuPDF |
| Frontend | React 19, Vite, Tailwind CSS |
| Auth | JWT (python-jose), bcrypt (passlib) |

## Prerequisites

- Docker & Docker Compose (recommended)
- **Or** locally: Python 3.12+, Node.js 20+, PostgreSQL 16 with pgvector
- A [Google Gemini API key](https://aistudio.google.com/apikey)

## Quick Start (Docker)

```bash
git clone <repo-url>
cd legal-rag
cp .env.example .env
# Edit .env — set GEMINI_API_KEY and SECRET_KEY at minimum
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| Readiness | http://localhost:8000/ready |

On startup the API container automatically runs `alembic upgrade head` and seeds the legal corpus from the root-level JSONL files.

### Preparing the corpus

Place (or keep) these files at the repository root:

| File | Description |
|------|-------------|
| `chunked_documents.jsonl` | Chunked legal text with metadata (required) |
| `embedded_documents.jsonl` | Pre-computed 384-dim embeddings (~564 MB for 57k chunks) |

**Option A — pre-generate embeddings (recommended for faster first boot):**

```bash
pip install -r backend/requirements.txt -r requirements.txt
python backend/scripts/generate_embeddings.py
```

**Option B — auto-generate on first Docker start** (default in `docker-compose.yml` via `GENERATE_EMBEDDINGS_ON_SEED=true`):

```bash
docker compose up --build
```

The first start may take 10–20 minutes while embeddings are computed for ~57k chunks. Subsequent starts reuse the persisted `corpus_data` volume.

To skip corpus loading entirely, set `SEED_CORPUS=false` in `.env`.

## Running Locally (without Docker)

### 1. Database

```bash
# Start PostgreSQL with pgvector (or use docker compose up db)
docker compose up db -d
```

### 2. Backend

```bash
cp .env.example .env
# Edit .env with your credentials

cd backend
pip install -r requirements.txt
pip install -r ../requirements.txt

alembic upgrade head
cd ..
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173 — set VITE_API_URL=http://localhost:8000 in .env if needed
```

## Environment Variables

Copy `.env.example` to `.env` at the repository root. Key variables:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Async PostgreSQL connection string |
| `GEMINI_API_KEY` | Google Gemini API key (required for chat) |
| `SECRET_KEY` | JWT signing secret (change in production) |
| `EMBEDDING_MODEL` | SentenceTransformer model name |
| `VITE_API_URL` | Backend URL for frontend (build-time for Docker) |
| `SEED_CORPUS` | Load pre-built corpus on startup (`true`/`false`) |
| `GENERATE_EMBEDDINGS_ON_SEED` | Generate `embedded_documents.jsonl` from chunked file if missing |
| `CHUNKED_DOCUMENTS_PATH` | Path to chunked JSONL (default: `./chunked_documents.jsonl`) |
| `EMBEDDED_DOCUMENTS_PATH` | Path to embedded JSONL (default: `./embedded_documents.jsonl`) |

See `.env.example` for the full grouped list.

## Authentication Flow

1. `POST /api/v1/auth/signup` — Register with email/password
2. `POST /api/v1/auth/login` — Returns JWT access token
3. Include `Authorization: Bearer <token>` on all protected endpoints
4. Documents and chat sessions are scoped to the authenticated user

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Register user |
| POST | `/api/v1/auth/login` | Login, get JWT |
| POST | `/api/v1/documents/upload` | Upload PDF |
| GET | `/api/v1/documents` | List user documents |
| POST | `/api/v1/retrieval/retrieve` | Similarity search |
| POST | `/api/v1/chat` | RAG chat with citations |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness (DB + pgvector) |

Full contracts: `docs/api-contracts.md`, interactive docs at `/docs`.

## Folder Structure

```
legal-rag/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/v1/    # HTTP routers
│   │   ├── services/  # Business logic
│   │   ├── models/    # SQLAlchemy models
│   │   └── repositories/
│   └── alembic/       # Database migrations
├── frontend/          # React + Vite UI
├── retrieval/         # Team B — vector search
├── rag_chat/          # Team C — LLM & citations
├── chunking/          # Team A — text chunking
├── docs/              # Architecture & API docs
├── docker-compose.yml
├── .env.example
└── requirements.txt   # Team A/B/C shared Python deps
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `503 Database not ready` on `/ready` | Wait for Postgres healthcheck; verify `DATABASE_URL` |
| `GEMINI_API_KEY not configured` | Set key in `.env`, restart API |
| Port 8000 in use | Change `BACKEND_PORT` or compose port mapping |
| Frontend can't reach API | Set `VITE_API_URL=http://localhost:8000` before `docker compose build frontend` |
| Migration errors | Run `cd backend && alembic upgrade head` manually |
| Corpus seed skipped | Ensure `chunked_documents.jsonl` exists at repo root; run `python backend/scripts/generate_embeddings.py` |
| First Docker start slow | Expected when generating embeddings; pre-generate locally or wait for completion |
| OCR fails on Linux | Ensure `libgl1` and `libglib2.0-0` are installed (included in Dockerfile) |

## Development

- **Team A (Ingestion)**: `backend/app/services/ingestion/ingestion_service.py`
- **Team B (Retrieval)**: `backend/app/services/retrieval/retrieval_service.py`
- **Team C (LLM/RAG)**: `backend/app/services/rag/rag_service.py`

Run backend tests:

```bash
cd backend
pytest
```

## License

See repository license file.
