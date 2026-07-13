# Backend Endpoints

All v1 endpoints are prefixed with `/api/v1`. Auth-protected endpoints require `Authorization: Bearer <token>`.

---

## Authentication (`/api/v1/auth`)

| Method   | Route                  | Description                                  | Auth |
|----------|------------------------|----------------------------------------------|------|
| `POST`   | `/auth/signup`         | Register a new user, returns JWT             | No   |
| `POST`   | `/auth/login`          | Authenticate with email/password, returns JWT| No   |
| `POST`   | `/auth/token`          | OAuth2 form-based login (Swagger UI)         | No   |
| `GET`    | `/auth/me`             | Get current authenticated user profile       | Yes  |

### `POST /auth/signup`

- **Request Body:** `{ "email": string, "password": string, "full_name"?: string }`
- **Response:** `TokenResponse { access_token: string, token_type: "bearer" }` — `201`

### `POST /auth/login`

- **Request Body:** `{ "email": string, "password": string }`
- **Response:** `TokenResponse` — `200`

### `POST /auth/token`

- **Request Body:** `application/x-www-form-urlencoded` — `username`, `password`
- **Response:** `TokenResponse` — `200`

### `GET /auth/me`

- **Response:** `UserResponse { id, email, full_name, is_active, created_at }` — `200`

---

## Documents (`/api/v1/documents`)

| Method   | Route                           | Description                                    | Auth |
|----------|---------------------------------|------------------------------------------------|------|
| `POST`   | `/documents/upload`             | Upload a document and start processing         | Yes  |
| `GET`    | `/documents`                    | List user's documents                          | Yes  |
| `GET`    | `/documents/{document_id}`      | Get a specific document                        | Yes  |
| `GET`    | `/documents/{document_id}/status` | Get processing job status                    | Yes  |

### `POST /documents/upload`

- **Content-Type:** `multipart/form-data`
- **Request Body:** `file` (UploadFile, required)
- **Response:** `UploadResponse { document_id: int, job_id: int, status: string }` — `200`

### `GET /documents`

- **Query Params:** `skip` (int, default 0), `limit` (int, default 100)
- **Response:** `List[DocumentResponse]` — `200`

### `GET /documents/{document_id}`

- **Path Params:** `document_id` (int)
- **Response:** `DocumentResponse` — `200`

### `GET /documents/{document_id}/status`

- **Path Params:** `document_id` (int)
- **Response:** `ProcessingJobResponse { id, document_id, stage, status, error_message, started_at, completed_at }` — `200`

---

## Extraction (`/api/v1/extraction`)

| Method   | Route                                  | Description                          | Auth |
|----------|----------------------------------------|--------------------------------------|------|
| `POST`   | `/extraction/process/{document_id}`    | Re-trigger processing pipeline       | Yes  |
| `GET`    | `/extraction/chunks/{document_id}`     | Get chunks for a document            | Yes  |

### `POST /extraction/process/{document_id}`

- **Path Params:** `document_id` (int)
- **Response:** `MessageResponse { message: string }` — `200`

### `GET /extraction/chunks/{document_id}`

- **Path Params:** `document_id` (int)
- **Response:** `List[ChunkResponse { id, document_id, content, chunk_index, created_at }]` — `200`

---

## Retrieval (`/api/v1/retrieval`)

| Method   | Route                     | Description                            | Auth |
|----------|---------------------------|----------------------------------------|------|
| `POST`   | `/retrieval/retrieve`     | Retrieve and rerank relevant chunks    | Yes  |

### `POST /retrieval/retrieve`

- **Request Body:** `{ "query": string, "top_k"?: int (default 5), "document_ids"?: int[] }`
- **Response:** `RetrievalResponse { query, results: [{ chunk_id, page_content, metadata, score }] }` — `200`

---

## Chat (`/api/v1/chat`)

| Method   | Route                            | Description                         | Auth |
|----------|----------------------------------|-------------------------------------|------|
| `POST`   | `/chat`                          | Send a message, get RAG response    | Yes  |
| `POST`   | `/chat/history`                  | Create a new chat session           | Yes  |
| `GET`    | `/chat/history/{session_id}`     | Get chat history for a session      | Yes  |
| `DELETE` | `/chat/history/{session_id}`     | Delete a chat session               | Yes  |
| `POST`   | `/chat/query-rewrite`            | Rewrite query using history         | Yes  |

### `POST /chat`

- **Request Body:** `{ "session_id"?: int, "message": string, "use_rag"?: bool }`
- **Response:** `ChatResponse { session_id, message: { id, role, content, created_at, citations } }` — `200`

### `POST /chat/history`

- **Request Body:** None
- **Response:** `ChatSessionResponse { id, title, created_at, updated_at }` — `200`

### `GET /chat/history/{session_id}`

- **Path Params:** `session_id` (int)
- **Response:** `List[ChatMessageResponse]` — `200`

### `DELETE /chat/history/{session_id}`

- **Path Params:** `session_id` (int)
- **Response:** `MessageResponse { message: string }` — `200`

### `POST /chat/query-rewrite`

- **Request Body:** `{ "query": string, "history": [{ "role": string, "content": string }] }`
- **Response:** `QueryRewriteResponse { rewritten_query: string }` — `200`

---

## System (root-level, no `/api/v1` prefix)

| Method | Route      | Description                                           | Auth |
|--------|------------|-------------------------------------------------------|------|
| `GET`  | `/health`  | Liveness check                                        | No   |
| `GET`  | `/ready`   | Deep readiness (DB + Pinecone + Embedding Service)    | No   |
