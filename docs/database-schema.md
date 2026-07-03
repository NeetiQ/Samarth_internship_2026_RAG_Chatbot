# Database Schema (V2)

The backend uses PostgreSQL with the `Pinecone` extension. 

## Tables

### 1. `documents`
Stores physical file representations and structured metadata.
- `id` (PK)
- `title`, `filename`, `file_type`, `file_path`
- **Structured Metadata**: `court`, `case_number`, `judgment_date`, `source`, `language`
- `created_at`, `updated_at`

### 2. `chunks`
Stores text chunks extracted from documents. **Embeddings are stored directly here.**
- `id` (PK)
- `document_id` (FK -> documents.id)
- `content` (Text)
- **Structured Metadata**: `page_number`, `section`, `paragraph`, `chunk_index`
- **Vector**: `embedding` (Pinecone 1024-dim)
- `created_at`

### 3. `processing_jobs`
Tracks asynchronous ingestion jobs.
- `id` (PK)
- `document_id` (FK -> documents.id)
- `stage` (Enum: UPLOADED, OCR, EXTRACTION, CLEANING, CHUNKING, EMBEDDING, COMPLETED, FAILED)
- `status` (String: pending, in_progress, completed, failed)
- `error_message` (Text)
- `started_at`, `completed_at`

### 4. `chat_sessions` & `chat_messages`
Stores user interactions with the LLM.
- **Sessions**: `id`, `title`, `created_at`, `updated_at`
- **Messages**: `id`, `session_id`, `role`, `content`, `created_at`

### 5. `citations`
Maps assistant messages back to the source chunks.
- `id` (PK)
- `message_id` (FK -> chat_messages.id)
- `chunk_id` (FK -> chunks.id)
- `score` (Float)

### 6. `prompt_logs`
For telemetry and prompt engineering debugging.
- `id` (PK)
- `session_id` (FK)
- `prompt_text`, `model`, `tokens_used`, `created_at`
