# Database Schema

The backend uses **PostgreSQL** (managed on Render) for relational data and **Pinecone** for vector storage.

---

## PostgreSQL Tables

### 1. `users`
Stores registered user accounts for JWT-based authentication.
- `id` (PK, Integer, auto-increment)
- `email` (String, unique, indexed)
- `hashed_password` (String — bcrypt hash via passlib)
- `created_at` (DateTime)

### 2. `documents`
Stores uploaded file metadata and structured legal metadata.
- `id` (PK, Integer, auto-increment)
- `title`, `filename`, `file_type`, `file_path`
- **Structured Metadata**: `court`, `case_number`, `judgment_date`, `source`, `language`
- `created_at`, `updated_at`

### 3. `chunks`
Stores text chunks extracted from documents.
- `id` (PK, Integer, auto-increment)
- `document_id` (FK → documents.id)
- `content` (Text)
- **Structured Metadata**: `page_number`, `section`, `paragraph`, `chunk_index`
- `created_at`

### 4. `processing_jobs`
Tracks asynchronous ingestion job stages.
- `id` (PK, Integer, auto-increment)
- `document_id` (FK → documents.id)
- `stage` (Enum: UPLOADED, OCR, EXTRACTION, CLEANING, CHUNKING, EMBEDDING, COMPLETED, FAILED)
- `status` (String: pending, in_progress, completed, failed)
- `error_message` (Text, nullable)
- `started_at`, `completed_at`

### 5. `chat_sessions`
Stores conversation sessions.
- `id` (PK, Integer, auto-increment)
- `title` (String)
- `created_at`, `updated_at`

### 6. `chat_messages`
Stores individual messages within a chat session.
- `id` (PK, Integer, auto-increment)
- `session_id` (FK → chat_sessions.id)
- `role` (String: "user" or "assistant")
- `content` (Text)
- `created_at`

### 7. `citations`
Maps assistant messages back to source chunks.
- `id` (PK, Integer, auto-increment)
- `message_id` (FK → chat_messages.id)
- `chunk_id` (FK → chunks.id)
- `score` (Float — relevance score)

### 8. `prompt_logs`
Telemetry for prompt engineering debugging.
- `id` (PK, Integer, auto-increment)
- `session_id` (FK → chat_sessions.id)
- `prompt_text` (Text)
- `model` (String)
- `tokens_used` (Integer)
- `created_at`

---

## Pinecone Vector Storage

Vectors are stored in Pinecone with the following structure:

```json
{
  "id": "chunk_12345",
  "values": [0.123, 0.456, ...],
  "metadata": {
    "document_id": "doc_123",
    "document_name": "Contract_A.pdf",
    "chunk_index": 5,
    "page_number": 2,
    "text": "...chunk text...",
    "document_type": "contract"
  }
}
```

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384
- **Similarity Metric**: Cosine

---

## Migrations

Managed via **Alembic** from the `backend/alembic/` directory.

```bash
# Apply all migrations
cd backend
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "description"
```

---

## ER Diagram

```
users
  │
  └── (auth only, not FK-linked to documents in current schema)

documents ─── 1:N ──── chunks
    │                      │
    │                      └── citations (chunk_id)
    │
    └── 1:N ──── processing_jobs

chat_sessions ─── 1:N ──── chat_messages
                                │
                                └── citations (message_id)
                                │
                                └── prompt_logs (session_id)
```
