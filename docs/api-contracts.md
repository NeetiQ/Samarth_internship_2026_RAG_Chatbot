# API Contracts

This document defines the core request and response schemas used across the Legal RAG Backend.

## Document Upload Response
```json
{
  "document_id": 1,
  "job_id": 1,
  "status": "uploaded"
}
```

## Retrieval Response
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

## Chat Request
```json
{
  "session_id": null,
  "message": "Explain the concept of force majeure.",
  "use_rag": true
}
```

## Chat Response
```json
{
  "session_id": 42,
  "message": {
    "id": 108,
    "role": "assistant",
    "content": "Force majeure is a contractual clause...",
    "created_at": "2026-06-26T15:00:00Z",
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

## Processing Job Status Response
```json
{
  "id": 1,
  "document_id": 1,
  "stage": "OCR",
  "status": "in_progress",
  "error_message": null,
  "started_at": "2026-06-26T15:00:00Z",
  "completed_at": null
}
```
