# System Architecture

> **Basis:** The pipeline flow (ingestion → retrieval → chat) is grounded in the source specifications. The auth/authorization layers wrapping it are **PROPOSED DESIGN**, added to reflect a single integrated, access-controlled backend rather than three open internal services.

## 1. Overview

Legal RAG System runs as **one FastAPI backend** serving a React frontend. It replaces what was originally specified as three separately-addressable services (ingestion, retrieval, chat — each with its own `/health` and duplicated `/documents` routes) with a single process, single database, and single set of endpoints. Internal calls between pipeline stages are now in-process function calls, not HTTP round-trips.

All ML inference (embedding generation and reranking) is **externalized** to the dedicated HF Inference Service hosted on Hugging Face Spaces. The backend never loads any ML model into memory.

## 2. High-Level Flow

```mermaid
graph TD
    U[User] --> FE[React Frontend]
    FE --> AUTH[JWT Authentication *proposed*]
    AUTH --> API[FastAPI Backend on Render]
    API --> AZ[Authorization Middleware *proposed*]
    AZ --> UP[Document Upload]
    UP --> OCR[OCR]
    OCR --> CLEAN[Text Cleaning]
    CLEAN --> CHUNK[Chunking]
    CHUNK --> HF_EMBED[HF Space /embed/document]
    HF_EMBED --> PGV[(Pinecone)]
    API --> HF_QUERY[HF Space /embed/query]
    HF_QUERY --> SEARCH[Pinecone Similarity Search]
    SEARCH --> HF_RERANK[HF Space /rerank]
    HF_RERANK --> PROMPT[Prompt Construction]
    PROMPT --> GEMINI[Gemini]
    GEMINI --> CITE[Citation Generation]
    CITE --> RESP[Response]
    RESP --> FE
```

## 3. Deployment Architecture

```
Frontend (Vercel)
       ↓
Render Backend (FastAPI — no ML models loaded)
       ↓
HF Space (Inference Service)
   ├── POST /embed/query    — SentenceTransformer embedding
   ├── POST /embed/document — Batch embedding
   └── POST /rerank         — CrossEncoder reranking
       ↓
Pinecone (Vector Store)
       ↓
Gemini (LLM)
```

## 4. Component Responsibilities

| Component | Responsibility | Basis |
|---|---|---|
| React Frontend | Upload UI, chat UI, session/history views | Proposed (mentioned only as "Team D" in source) |
| JWT Authentication | Verifies identity on every request | Proposed |
| Authorization Middleware | Resolves `current_user`, enforces ownership | Proposed |
| Ingestion Pipeline | OCR → clean → chunk → embed (via HF) → store | Source doc |
| Retrieval Module | Query embedding (via HF) → Pinecone search → Rerank (via HF) → Top-K chunks | Source doc |
| HF Inference Service | `SentenceTransformer` embedding + `CrossEncoder` reranking | This migration |
| RAG Chat Module | Prompt construction, Gemini call, citation generation, history | Source doc |
| Pinecone Store | Vector index over document chunks | Source doc |

## 5. Why One Integrated Backend

The original three-service split (ingestion / retrieval / chat) required duplicated endpoints — each service independently exposed `GET /documents`, `DELETE /documents/{id}`, and `GET /health` — and Team C depended on an HTTP call to Team B's `/retrieve` endpoint for every chat turn. Consolidating into a single backend:

- Removes duplicate document-management endpoints (see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md))
- Turns the chat → retrieval network hop into a direct function call, reducing latency
- Gives ownership/authorization a single enforcement point instead of three
- Simplifies deployment to one service instead of three independently versioned ones

## 6. Request Lifecycle

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as FastAPI Backend
    participant HF as HF Space
    participant PC as Pinecone
    participant G as Gemini

    U->>FE: Ask question
    FE->>API: POST /api/v1/chat (Bearer token)
    API->>API: Validate JWT, resolve current_user
    API->>HF: POST /embed/query
    HF-->>API: Query embedding vector
    API->>PC: Similarity search (cosine, Top-K)
    PC-->>API: Top-K chunks + metadata
    API->>HF: POST /rerank {query, documents}
    HF-->>API: Ranked [{index, score}]
    API->>API: Construct prompt (context + history)
    API->>G: Generate response
    G-->>API: Answer text
    API->>API: Build citations from chunk metadata
    API-->>FE: Answer + citations
    FE-->>U: Render response
```

## 7. Environment Variables

### Backend (Render)

| Variable | Purpose | Default |
|---|---|---|
| `EMBEDDING_SERVICE_URL` | Base URL for HF Space (used for `/embed/*`) | `http://localhost:7860` |
| `EMBEDDING_SERVICE_API_KEY` | Shared Bearer token for HF service auth | — |
| `RERANKER_SERVICE_URL` | Base URL for reranker (same HF Space host) | same as above |
| `REQUEST_TIMEOUT` | HTTP timeout (seconds) for all HF service calls | `30` |
| `RERANKER_ENABLED` | Toggle reranking on/off | `true` |

### HF Inference Service

| Variable | Purpose | Default |
|---|---|---|
| `MODEL_NAME` | Embedding model name | `all-MiniLM-L6-v2` |
| `RERANKER_MODEL` | CrossEncoder model name | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `EMBEDDING_SERVICE_API_KEY` | Bearer token for request authentication | — |

## 8. Related Documents

- [RAG_PIPELINE.md](./RAG_PIPELINE.md) — stage-by-stage pipeline detail
- [DATABASE_DESIGN.md](./DATABASE_DESIGN.md) — schema backing this architecture
- [SECURITY.md](./SECURITY.md) — how ownership is enforced at each layer
- [WORKFLOW_DIAGRAMS.md](./WORKFLOW_DIAGRAMS.md) — additional diagrams
