# API Contracts

This document defines the core request and response schemas used across the Legal RAG Backend.

**Base URL**: `https://legal-rag-backend-zf50.onrender.com`
**API Prefix**: `/api/v1`

---

## Authentication

### POST `/api/v1/auth/signup`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (201):
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-07-06T12:00:00Z"
}
```

### POST `/api/v1/auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

> All subsequent requests must include the header: `Authorization: Bearer <access_token>`

---

## Document Upload

### POST `/api/v1/documents/upload`

**Request**: `multipart/form-data` with file field

**Response** (200):
```json
{
  "document_id": 1,
  "job_id": 1,
  "status": "uploaded"
}
```

### GET `/api/v1/documents/{document_id}/status`

**Response** (200):
```json
{
  "id": 1,
  "document_id": 1,
  "stage": "EMBEDDING",
  "status": "in_progress",
  "error_message": null,
  "started_at": "2026-07-06T15:00:00Z",
  "completed_at": null
}
```

---

## Retrieval

### POST `/api/v1/retrieval/retrieve`

**Request**:
```json
{
  "query": "What is the penalty for breach of contract?",
  "top_k": 5
}
```

**Response** (200):
```json
{
  "query": "What is the penalty for breach of contract?",
  "results": [
    {
      "chunk_id": 105,
      "document_id": 2,
      "content": "A breach of contract under section...",
      "score": 0.92,
      "page_number": 12,
      "section": "Remedies",
      "paragraph": 3
    }
  ]
}
```

---

## Chat

### POST `/api/v1/chat`

**Request**:
```json
{
  "session_id": null,
  "message": "Explain the concept of force majeure.",
  "use_rag": true
}
```

**Response** (200):
```json
{
  "session_id": 42,
  "message": {
    "id": 108,
    "role": "assistant",
    "content": "Force majeure is a contractual clause...",
    "created_at": "2026-07-06T15:00:00Z",
    "citations": [
      {
        "chunk_id": 105,
        "score": 0.88,
        "content": "...",
        "document_id": 2
      }
    ]
  }
}
```

### POST `/api/v1/chat/history`

**Request**:
```json
{
  "title": "Contract Law Discussion"
}
```

**Response** (201):
```json
{
  "session_id": 43,
  "title": "Contract Law Discussion",
  "created_at": "2026-07-06T15:00:00Z"
}
```

### GET `/api/v1/chat/history/{session_id}`

**Response** (200):
```json
{
  "session_id": 42,
  "messages": [
    {
      "id": 107,
      "role": "user",
      "content": "Explain the concept of force majeure.",
      "created_at": "2026-07-06T14:59:00Z"
    },
    {
      "id": 108,
      "role": "assistant",
      "content": "Force majeure is a contractual clause...",
      "created_at": "2026-07-06T15:00:00Z"
    }
  ]
}
```

---

## System

### GET `/health`

**Response** (200):
```json
{
  "status": "ok",
  "project": "Legal RAG System"
}
```

### GET `/ready`

**Response** (200):
```json
{
  "status": "ready",
  "project": "Legal RAG System"
}
```

**Response** (503 — if database is unreachable):
```json
{
  "detail": "Database not ready"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error description here"
}
```

| Status Code | Description                      |
| ----------- | -------------------------------- |
| 400         | Bad Request / Validation Error   |
| 401         | Unauthorized (missing/bad token) |
| 403         | Forbidden                        |
| 404         | Resource Not Found               |
| 422         | Unprocessable Entity             |
| 500         | Internal Server Error            |
| 503         | Service Unavailable              |
