# API Contracts

TBD - Add API contract definitions and specifications here.

## Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

---

## Chat API

### Send Message

**Endpoint**: `POST /api/chat`

**Request**:
```json
{
  "conversation_id": "conv_123",
  "message": "What are the payment terms?",
  "session_id": "sess_456",
  "stream": false
}
```

**Response** (200 OK):
```json
{
  "id": "msg_789",
  "content": "According to the contract, payment terms are...",
  "citations": [
    {
      "text": "Net 30 from invoice date",
      "source": "contract_a.pdf",
      "page": 2,
      "chunk_id": "chunk_123"
    }
  ],
  "metadata": {
    "processing_time_ms": 2340,
    "model_used": "gpt-4",
    "tokens_used": 1523
  }
}
```

**Response** (400 Bad Request):
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Message content cannot be empty",
    "details": {}
  }
}
```

---

## Ingestion API

### Upload Document

**Endpoint**: `POST /api/ingest`

**Request**: (multipart/form-data)
```
file: <PDF or text file>
document_type: "contract" | "agreement" | "policy" | "other"
metadata: {"case_id": "123", "date": "2024-01-01"}
```

**Response** (202 Accepted):
```json
{
  "job_id": "ingest_job_xyz",
  "status": "processing",
  "filename": "contract.pdf",
  "estimated_completion": "2024-01-15T10:30:00Z"
}
```

### Get Ingestion Status

**Endpoint**: `GET /api/ingest/{job_id}`

**Response** (200 OK):
```json
{
  "job_id": "ingest_job_xyz",
  "status": "completed",
  "filename": "contract.pdf",
  "chunks_created": 42,
  "embedding_status": "completed",
  "errors": [],
  "completed_at": "2024-01-15T10:35:00Z"
}
```

---

## Retrieval API

### Search Documents

**Endpoint**: `GET /api/retrieval/search`

**Query Parameters**:
```
q: string (search query)
top_k: integer (default: 5, max: 20)
document_id: string (optional, filter by document)
filter: string (optional, JSON filter)
```

**Response** (200 OK):
```json
{
  "query": "payment terms",
  "results": [
    {
      "id": "chunk_123",
      "text": "Payment terms are Net 30...",
      "score": 0.892,
      "document": {
        "id": "doc_456",
        "name": "contract_a.pdf",
        "type": "contract"
      },
      "page": 2,
      "position": "middle"
    }
  ],
  "total_results": 12,
  "processing_time_ms": 234
}
```

---

## Conversation API

### Create Conversation

**Endpoint**: `POST /api/conversations`

**Request**:
```json
{
  "title": "Contract Review - ABC Inc",
  "documents": ["doc_123", "doc_456"]
}
```

**Response** (201 Created):
```json
{
  "id": "conv_789",
  "title": "Contract Review - ABC Inc",
  "created_at": "2024-01-15T10:00:00Z",
  "documents": ["doc_123", "doc_456"]
}
```

### Get Conversation History

**Endpoint**: `GET /api/conversations/{conversation_id}`

**Response** (200 OK):
```json
{
  "id": "conv_789",
  "title": "Contract Review - ABC Inc",
  "messages": [
    {
      "id": "msg_1",
      "role": "user",
      "content": "What are the payment terms?",
      "created_at": "2024-01-15T10:05:00Z"
    },
    {
      "id": "msg_2",
      "role": "assistant",
      "content": "According to the contract...",
      "citations": [...],
      "created_at": "2024-01-15T10:05:30Z"
    }
  ]
}
```

---

## Document Management API

### List Documents

**Endpoint**: `GET /api/documents`

**Query Parameters**:
```
page: integer (default: 1)
limit: integer (default: 20)
type: string (optional, filter by type)
```

**Response** (200 OK):
```json
{
  "documents": [
    {
      "id": "doc_123",
      "filename": "contract_a.pdf",
      "type": "contract",
      "upload_date": "2024-01-15T10:00:00Z",
      "size_bytes": 1024000,
      "chunks_count": 42,
      "status": "processed"
    }
  ],
  "total": 156,
  "page": 1,
  "pages": 8
}
```

### Delete Document

**Endpoint**: `DELETE /api/documents/{document_id}`

**Response** (204 No Content)

---

## Health & Metrics API

### Health Check

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "services": {
    "database": "connected",
    "vectordb": "connected",
    "llm": "connected",
    "cache": "connected"
  }
}
```

### Metrics

**Endpoint**: `GET /metrics`

**Response** (200 OK):
```
# Prometheus format
legal_rag_api_requests_total{method="GET",endpoint="/search",status="200"} 1234
legal_rag_api_request_duration_seconds_bucket{endpoint="/search",le="0.5"} 890
legal_rag_ingestion_chunks_total{document_type="contract"} 45678
legal_rag_vector_db_latency_ms{operation="search"} 234
```

---

## WebSocket API (Streaming)

### Chat Stream

**Endpoint**: `WS /api/chat/stream`

**Connection Message**:
```json
{
  "type": "connect",
  "conversation_id": "conv_123",
  "session_id": "sess_456"
}
```

**Message Message**:
```json
{
  "type": "message",
  "content": "What are the key obligations?"
}
```

**Server Stream** (tokens):
```json
{
  "type": "stream",
  "delta": "According",
  "citations_chunk": null
}
```

**Server Citations** (chunk):
```json
{
  "type": "citations",
  "citation": {
    "text": "Key obligations include...",
    "source": "contract.pdf",
    "page": 3
  }
}
```

**Server Done**:
```json
{
  "type": "done",
  "message_id": "msg_999",
  "total_tokens": 342
}
```

---

## Status Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 200  | OK                                      |
| 201  | Created                                 |
| 202  | Accepted (async processing)             |
| 204  | No Content                              |
| 400  | Bad Request                             |
| 401  | Unauthorized                            |
| 403  | Forbidden                               |
| 404  | Not Found                               |
| 409  | Conflict                                |
| 422  | Unprocessable Entity (validation error) |
| 429  | Too Many Requests (rate limited)        |
| 500  | Internal Server Error                   |
| 503  | Service Unavailable                     |

---

## Rate Limiting

- **Free tier**: 100 requests/hour
- **Pro tier**: 10,000 requests/hour
- **Enterprise**: Unlimited

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1705318800
```
