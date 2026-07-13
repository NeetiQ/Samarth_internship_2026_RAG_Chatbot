# API Contract

## Overview

The Legal RAG API is a RESTful backend that provides programmatic access to the Legal RAG system. It enables user authentication, document management, text extraction, semantic retrieval, and RAG-powered chat over Indian legal documents.

The API follows REST architectural principles with JSON as the communication format. All endpoints are versioned under `/api/v1` to support future backward-compatible changes without breaking existing clients.

- **Base URL:** `https://<backend-host>/api/v1`
- **Protocol:** HTTPS (production), HTTP (development)
- **Format:** JSON request/response bodies
- **API Version:** `v1`

## Authentication

All endpoints except `/health`, `/ready`, and `/api/v1/auth/*` require a JWT Bearer token.

**How JWT authentication works:**

1. The client authenticates via `POST /api/v1/auth/login` or `POST /api/v1/auth/signup`.
2. The server returns a signed JWT access token (HS256, 60-minute expiry).
3. The client includes the token in all subsequent requests via the `Authorization` header.
4. The server validates the token, extracts the user identity, and enforces ownership on resources.

**Public endpoints** (no token required): `/health`, `/ready`, `/api/v1/auth/signup`, `/api/v1/auth/login`, `/api/v1/auth/token`.

**Protected endpoints** (token required): All document, extraction, retrieval, and chat endpoints.

| Header          | Value              |
|-----------------|--------------------|
| `Authorization` | `Bearer <token>`   |
| `Content-Type`  | `application/json` |

## Request/Response Conventions

- **Format:** All request and response bodies use JSON (`application/json`), except file uploads which use `multipart/form-data`.
- **Authorization:** Protected endpoints require `Authorization: Bearer <token>` header.
- **Pagination:** List endpoints support `skip` and `limit` query parameters (e.g., `GET /documents?skip=0&limit=100`).
- **File Uploads:** Document upload uses `multipart/form-data` with a `file` field. Max upload size is 50 MB.

## Error Handling

All errors follow a consistent JSON structure:

```json
{
  "error": "Error Category",
  "message": "Human-readable description"
}
```

**Validation errors** (422) include field-level details from Pydantic:

```json
{
  "error": "Validation Error",
  "details": [
    { "loc": ["body", "email"], "msg": "field required", "type": "value_error.missing" }
  ]
}
```

**Authentication errors** (401) are returned when the JWT is missing, expired, or invalid:

```json
{
  "error": "Unauthorized",
  "message": "Could not validate credentials"
}
```

**Database errors** (500) are logged server-side and return a generic message to avoid leaking internals.

## Standard HTTP Status Codes

| Code | Meaning                |
|------|------------------------|
| 200  | Success                |
| 201  | Created                |
| 400  | Bad Request            |
| 401  | Unauthorized           |
| 403  | Forbidden              |
| 404  | Not Found              |
| 409  | Conflict               |
| 422  | Validation Error       |
| 500  | Internal Server Error  |
| 503  | Service Unavailable    |

## Endpoint Organization

Endpoints are grouped by domain responsibility:

| Group          | Purpose                                                        |
|----------------|----------------------------------------------------------------|
| **Auth**       | User registration, login, token management, profile retrieval  |
| **Documents**  | Upload, list, and inspect legal documents and processing status|
| **Extraction** | Re-trigger processing pipelines and retrieve extracted chunks  |
| **Retrieval**  | Semantic search and reranking over the legal corpus            |
| **Chat**       | RAG-powered Q&A with session management and citations          |
| **Health**     | Liveness and readiness probes for monitoring and deployment    |

## Best Practices

- The API is **stateless** — each request carries all information needed for processing (JWT token, request body). No server-side sessions are stored.
- **GET requests are idempotent** — they can be safely retried without side effects.
- Standard **HTTP status codes** indicate success or failure. Clients should handle 4xx and 5xx responses gracefully.

---

## Endpoint Groups

### Authentication

#### `POST /api/v1/auth/signup`

Register a new user.

```json
// Request
{ "email": "user@example.com", "password": "s3cret", "full_name": "John Doe" }

// Response 201
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

#### `POST /api/v1/auth/login`

Authenticate with email and password.

```json
// Request
{ "email": "user@example.com", "password": "s3cret" }

// Response 200
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

#### `POST /api/v1/auth/token`

OAuth2-compatible token endpoint (used by Swagger UI Authorize button). Accepts `application/x-www-form-urlencoded` with `username` and `password` fields.

#### `GET /api/v1/auth/me`

Returns the authenticated user's profile.

```json
// Response 200
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-07-01T12:00:00"
}
```

---

### Documents

#### `POST /api/v1/documents/upload`

Upload a document (PDF/image) and trigger background processing.

- **Content-Type:** `multipart/form-data`
- **Field:** `file` (required)

```json
// Response 200
{ "document_id": 42, "job_id": 7, "status": "processing" }
```

#### `GET /api/v1/documents`

List documents owned by or shared with the current user.

- **Query:** `skip` (int, default 0), `limit` (int, default 100)

```json
// Response 200
[
  {
    "id": 42, "title": "Supreme Court Judgment", "filename": "sc_2024_001.pdf",
    "file_type": "application/pdf", "court": "Supreme Court", "case_number": "SLP/2024/001",
    "judgment_date": null, "source": null, "language": "en",
    "file_path": "./data/uploads/sc_2024_001.pdf",
    "created_at": "2026-07-01T12:00:00", "updated_at": "2026-07-01T12:00:00"
  }
]
```

#### `GET /api/v1/documents/{document_id}`

Get details for a specific document (ownership verified).

#### `GET /api/v1/documents/{document_id}/status`

Poll the processing job status for a document.

```json
// Response 200
{
  "id": 7, "document_id": 42, "stage": "COMPLETED",
  "status": "completed", "error_message": null,
  "started_at": "2026-07-01T12:00:00", "completed_at": "2026-07-01T12:01:30"
}
```

---

### Extraction

#### `POST /api/v1/extraction/process/{document_id}`

Re-trigger the processing pipeline for a document.

```json
// Response 200
{ "message": "Processing pipeline initiated" }
```

#### `GET /api/v1/extraction/chunks/{document_id}`

Get all chunks extracted from a document.

```json
// Response 200
[
  {
    "id": 1, "document_id": 42, "content": "The court held that...",
    "chunk_index": 0, "created_at": "2026-07-01T12:01:00"
  }
]
```

---

### Retrieval

#### `POST /api/v1/retrieval/retrieve`

Retrieve and rerank relevant chunks from the shared corpus.

```json
// Request
{ "query": "What is the limitation period for civil suits?", "top_k": 5 }

// Response 200
{
  "query": "What is the limitation period for civil suits?",
  "results": [
    {
      "chunk_id": "chunk_abc123", "page_content": "Section 3 of the Limitation Act...",
      "metadata": { "source": "limitation_act.pdf", "page": 2 }, "score": 0.92
    }
  ]
}
```

---

### Chat

#### `POST /api/v1/chat`

Send a message and receive a RAG-augmented response with citations.

```json
// Request
{ "session_id": 1, "message": "Explain Section 498A IPC", "use_rag": true }

// Response 200
{
  "session_id": 1,
  "message": {
    "id": 0, "role": "assistant",
    "content": "Section 498A of the IPC deals with...",
    "created_at": "2026-07-01T12:05:00",
    "citations": [
      { "chunk_id": "chunk_xyz", "score": 0.89, "content": "...", "document_id": "42" }
    ]
  }
}
```

#### `POST /api/v1/chat/history`

Create a new chat session.

```json
// Response 200
{ "id": 5, "title": "New Session", "created_at": "...", "updated_at": "..." }
```

#### `GET /api/v1/chat/history/{session_id}`

Get all messages in a chat session (ownership verified).

#### `DELETE /api/v1/chat/history/{session_id}`

Delete a chat session (ownership verified).

```json
// Response 200
{ "message": "Session deleted successfully" }
```

#### `POST /api/v1/chat/query-rewrite`

Rewrite a user query using conversation history.

```json
// Request
{ "query": "What about the penalties?", "history": [{ "role": "user", "content": "Explain Section 498A" }] }

// Response 200
{ "rewritten_query": "What are the penalties under Section 498A IPC?" }
```

---

### Health

#### `GET /health`

Basic liveness check (no auth required).

```json
{ "status": "ok", "project": "Legal RAG API" }
```

#### `GET /ready`

Deep readiness check — verifies PostgreSQL, Pinecone, and Embedding Service connectivity.

```json
// 200 — all healthy
{
  "status": "ready", "project": "Legal RAG API",
  "components": { "database": "healthy", "pinecone": "healthy", "embedding_service": "healthy" }
}

// 503 — partial failure
{
  "detail": { "message": "System not ready", "components": { "pinecone": "Pinecone connection failed: ..." } }
}
```
