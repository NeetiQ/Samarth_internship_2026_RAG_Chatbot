# Legal RAG System — Release Candidate 1

> **📌 Source.** This documentation suite has been updated against the real codebase at
> [`NeetiQ/Samarth_internship_2026_RAG_Chatbot`, branch `release/v1.0-rc1`](https://github.com/NeetiQ/Samarth_internship_2026_RAG_Chatbot/tree/release/v1.0-rc1),
> replacing the earlier speculative "PROPOSED DESIGN" version of this suite. Where the shipped
> code differs from what a reasonable design would predict (missing endpoints, unscoped
> retrieval, mismatched chunk sizes, etc.) it is called out explicitly rather than smoothed over.

A full-stack Legal Retrieval-Augmented Generation (RAG) assistant. Upload legal PDFs, run OCR
and chunking, store embeddings in PGVector, retrieve relevant passages, and chat with
Gemini-powered answers that include citations.

## What This System Does

1. A user uploads a legal PDF via `POST /api/v1/documents/upload`.
2. A background task (`IngestionService`) extracts text (`pdf_extractor.py`), cleans it
   (`text_cleaner.py`), splits it into chunks (`chunking/chunker.py`, **500 characters / 50
   character overlap** via LangChain's `RecursiveCharacterTextSplitter`), embeds each chunk
   (`retrieval/embeddings/embedder.py`, `BAAI/bge-small-en-v1.5`, 384 dimensions, normalized),
   and writes the result to the `legal_chunks` table in PostgreSQL/PGVector.
3. A user asks a question via `POST /api/v1/chat`. The backend embeds the query, runs a cosine
   similarity search over PGVector (`retrieval/search/retriever.py`), builds a prompt
   (`rag_chat/prompts/prompt_builder.py`), and calls Gemini (`rag_chat/llm/gemini_client.py`).
4. The answer and citations (built directly from the retrieved chunks) are returned to the
   frontend.

## Features

- **Authentication** — JWT-based signup/login (`app_users` table), bcrypt password hashing
- **PDF Upload & OCR ingestion path** — background processing job per document, polled via a
  status endpoint
- **Chunking & Embeddings** — LangChain text splitting + SentenceTransformer embeddings
- **PGVector Retrieval** — cosine similarity search (`embedding <=> query_embedding`)
- **Gemini LLM Chat** — session-based chat with citation objects attached to each answer
- **React Frontend** — dashboard, upload, chat, case-comparison, and settings pages

## Architecture

```
┌─────────────┐     JWT      ┌───────────────────┐
│   React     │ ──────────►  │  FastAPI Backend  │
│  Frontend   │              │  (backend/app)    │
└─────────────┘              └─────────┬──────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              ┌──────────┐      ┌──────────────┐    ┌──────────────┐
              │PostgreSQL│      │ chunking/ +  │    │  rag_chat/   │
              │ PGVector │      │ retrieval/   │    │  (Gemini +   │
              │          │      │ (ingestion & │    │  citations)  │
              │          │      │  search)     │    │              │
              └──────────┘      └──────────────┘    └──────────────┘
```

The repository was originally built as separately-developed modules — `chunking/`,
`retrieval/`, `rag_chat/`, and an early `ingestion/` package — referred to in code comments as
"Team A/B/C" work. In this release they are **not separate services**: `backend/app/services/`
imports them directly (via `sys.path` manipulation) and calls their classes in-process from a
single FastAPI app. There is no ingestion/retrieval/chat network hop.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.116, SQLAlchemy 2 (async, `asyncpg`), Alembic |
| Database | PostgreSQL 16 + `pgvector/pgvector:pg16` image |
| Embeddings | `sentence-transformers` 5.0, `BAAI/bge-small-en-v1.5` (384-dim) |
| LLM | Google Gemini via `google-genai`, default model `gemini-2.5-flash` |
| OCR / extraction | PyMuPDF (`pdf_extractor.py`); `paddleocr` is a backend dependency but is not
  wired into the live ingestion path in this release — text extraction currently runs through
  `pdf_extractor.extract_pdf_pages` only |
| Frontend | React 19, Vite, Tailwind CSS |
| Auth | JWT (`python-jose`), bcrypt (`passlib`) |

## Prerequisites

- Docker & Docker Compose (recommended)
- **Or** locally: Python 3.12+, Node.js 20+, PostgreSQL 16 with the `pgvector` extension
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
|---|---|
| Frontend | http://localhost:3000 (served via nginx in the Docker build; dev server is 5173) |
| Backend API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| Readiness | http://localhost:8000/ready |

On startup, `backend/entrypoint.sh` runs `alembic upgrade head` and then attempts
`backend/scripts/seed_corpus.py` to load a pre-built legal corpus. If the corpus files aren't
present, seeding is skipped with a warning rather than failing the boot.

### Preparing the corpus

Place (or keep) these files at the repository root:

| File | Description |
|---|---|
| `chunked_documents.jsonl` | Chunked legal text with metadata (required for seeding) |
| `embedded_documents.jsonl` | Pre-computed 384-dim embeddings |

**Option A — pre-generate embeddings (recommended for a faster first boot):**

```bash
pip install -r backend/requirements.txt -r requirements.txt
python backend/scripts/generate_embeddings.py
```

**Option B — auto-generate on first Docker start** (`GENERATE_EMBEDDINGS_ON_SEED=true`):

```bash
docker compose up --build
```

To skip corpus loading entirely, set `SEED_CORPUS=false` in `.env`. Seeded corpus rows are
inserted with `is_shared=true` (see `backend/scripts/seed_corpus.py`).

## Running Locally (without Docker)

### 1. Database

```bash
docker compose up db -d
```

### 2. Backend

```bash
cp .env.example .env
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
# Opens at http://localhost:5173 — set VITE_API_URL=http://localhost:8000 if needed
```

## Environment Variables

Key settings, from `backend/app/core/settings.py`:

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/legal_rag` | Async PostgreSQL connection string |
| `SECRET_KEY` | `CHANGE-ME-IN-PRODUCTION` | JWT signing secret — **must** be changed for production |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT lifetime |
| `GEMINI_API_KEY` | *(empty)* | Required for `/api/v1/chat` to function |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model name |
| `EMBEDDING_MODEL_NAME` | `BAAI/bge-small-en-v1.5` | SentenceTransformer model |
| `EMBEDDING_DIMENSION` | `384` | Must match the model's output size and the `legal_chunks.embedding` column |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `500` / `50` | Characters per chunk / overlap |
| `SEED_CORPUS` | `true` | Load the pre-built corpus on startup |
| `GENERATE_EMBEDDINGS_ON_SEED` | `false` | Generate `embedded_documents.jsonl` if missing |
| `VITE_API_URL` | `http://localhost:8000` | Backend base URL (build-time for the frontend Docker image) |

See `.env.example` for the full grouped list.

## Authentication Flow

1. `POST /api/v1/auth/signup` — register with email/password, returns a JWT immediately
2. `POST /api/v1/auth/login` — returns a JWT access token
3. `GET /api/v1/auth/me` — returns the current user's profile
4. Include `Authorization: Bearer <token>` on all other endpoints
5. Documents and chat sessions are scoped to the authenticated user via `user_id`

> There is no server-side `/api/v1/auth/logout` route in this release. Logout is entirely
> client-side: the frontend removes the token from `localStorage` (see `frontend/src/services/api.js`).

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/signup` | Register user, returns JWT |
| POST | `/api/v1/auth/login` | Login, returns JWT |
| GET | `/api/v1/auth/me` | Current user profile |
| POST | `/api/v1/documents/upload` | Upload PDF, queues background processing |
| GET | `/api/v1/documents` | List documents (own + shared) |
| GET | `/api/v1/documents/{document_id}` | Document details |
| GET | `/api/v1/documents/{document_id}/status` | Poll processing job stage |
| POST | `/api/v1/extraction/process/{document_id}` | Manually re-trigger the pipeline |
| GET | `/api/v1/extraction/chunks/{document_id}` | List a document's chunks |
| POST | `/api/v1/retrieval/retrieve` | Similarity search |
| POST | `/api/v1/chat` | RAG chat with citations |
| POST | `/api/v1/chat/history` | Create a new chat session |
| GET | `/api/v1/chat/history/{session_id}` | Get session history |
| DELETE | `/api/v1/chat/history/{session_id}` | Delete a session |
| POST | `/api/v1/chat/query-rewrite` | Rewrite a follow-up query (currently a pass-through, see [RAG_PIPELINE.md](./RAG_PIPELINE.md)) |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness (DB + pgvector extension) |

There is **no** `DELETE /api/v1/documents/{document_id}` endpoint in this release — uploaded
documents cannot currently be deleted through the API. Full contracts:
[API_DOCUMENTATION.md](./API_DOCUMENTATION.md), interactive docs at `/docs`.

## Folder Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for the full, verified repository layout.

## Known Gaps in This Release

- **Retrieval is not scoped by user or by document ownership.** `retrieval/search/retriever.py`
  and `retrieval/vectordb/pgvector_store.py` run a plain cosine-similarity query over the entire
  `legal_chunks` table. Chat and `/api/v1/retrieval/retrieve` can therefore surface chunks from
  *any* user's private uploads, not just the shared corpus and the requesting user's own
  documents. See [SECURITY.md](./SECURITY.md).
- **Reranking is a no-op.** `retrieval/reranker/` exists but its `rerank()` method returns the
  input unchanged; it isn't invoked by `RetrievalService.full_retrieve` in any case.
- **Query rewriting is a no-op.** `RagService.rewrite_query` returns the query unmodified.
- **Document deletion is not implemented** at the API layer.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `503 Database not ready` on `/ready` | Missing `DATABASE_URL` or DB not ready | Check `.env`; ensure `db` passes its healthcheck before `api` starts |
| `vector` type not found | PGVector extension not enabled | `CREATE EXTENSION IF NOT EXISTS vector;` on the target database |
| 401 on every request | Wrong/rotated `SECRET_KEY` between restarts | Keep `SECRET_KEY` stable across deploys |
| `GEMINI_API_KEY not configured or invalid` | Missing/invalid Gemini key | Set `GEMINI_API_KEY` in `.env`, restart the API |
| Corpus seed skipped | `chunked_documents.jsonl` missing at repo root | Run `python backend/scripts/generate_embeddings.py`, or accept the warning and seed later |
| First Docker start slow | Embeddings being generated for the corpus | Pre-generate locally, or wait — `healthcheck.start_period` is set to 3600s to allow for this |

## Development

- Chunking module: `chunking/chunker.py`, `chunking/config.py`
- Retrieval module: `retrieval/search/retriever.py`, `retrieval/vectordb/`, `retrieval/embeddings/`
- RAG/chat module: `rag_chat/prompts/`, `rag_chat/llm/gemini_client.py`, `rag_chat/citations/`
- Backend integration layer: `backend/app/services/ingestion/ingestion_service.py`,
  `backend/app/services/retrieval/retrieval_service.py`, `backend/app/services/rag/rag_service.py`

Run backend tests:

```bash
cd backend
pytest
```

Module-level test suites also exist under `retrieval/tests/` and `rag_chat/tests/`.

## License

See repository license file.