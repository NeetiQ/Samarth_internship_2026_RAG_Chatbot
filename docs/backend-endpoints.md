# Backend API Endpoints

Interactive Swagger UI is available at `/api/v1/docs` on the running backend.

**Production Base URL**: `https://legal-rag-backend-zf50.onrender.com`

---

## Authentication (`/api/v1/auth`)

| Method | Endpoint                  | Description                          | Auth Required |
| ------ | ------------------------- | ------------------------------------ | ------------- |
| POST   | `/api/v1/auth/signup`     | Register a new user                  | No            |
| POST   | `/api/v1/auth/login`      | Login and receive JWT token          | No            |
| GET    | `/api/v1/auth/me`         | Get current authenticated user info  | Yes           |

## Documents & Ingestion (`/api/v1/documents`)

| Method | Endpoint                                 | Description                              | Auth Required |
| ------ | ---------------------------------------- | ---------------------------------------- | ------------- |
| POST   | `/api/v1/documents/upload`               | Upload a file and trigger processing     | Yes           |
| GET    | `/api/v1/documents`                      | List all uploaded documents              | Yes           |
| GET    | `/api/v1/documents/{document_id}`        | Get document details and metadata        | Yes           |
| GET    | `/api/v1/documents/{document_id}/status` | Poll the processing job stage            | Yes           |

## Extraction (`/api/v1/extraction`)

| Method | Endpoint                                        | Description                             | Auth Required |
| ------ | ------------------------------------------------ | --------------------------------------- | ------------- |
| POST   | `/api/v1/extraction/process/{document_id}`       | Manually re-trigger ingestion pipeline  | Yes           |

## Retrieval (`/api/v1/retrieval`)

| Method | Endpoint                      | Description                                         | Auth Required |
| ------ | ----------------------------- | --------------------------------------------------- | ------------- |
| POST   | `/api/v1/retrieval/retrieve`  | Perform semantic similarity search. Expects `query` and `top_k`. | Yes |

## Chat & LLM (`/api/v1/chat`)

| Method | Endpoint                             | Description                                          | Auth Required |
| ------ | ------------------------------------ | ---------------------------------------------------- | ------------- |
| POST   | `/api/v1/chat`                       | Send message to Gemini. If `use_rag=true`, fetches context from Retrieval. | Yes |
| POST   | `/api/v1/chat/history`               | Create a new chat session                            | Yes           |
| GET    | `/api/v1/chat/history/{session_id}`  | Retrieve past messages for a session                 | Yes           |
| POST   | `/api/v1/chat/query-rewrite`         | Rewrite query based on chat history before searching | Yes           |

## System (Root-Level)

| Method | Endpoint  | Description                                    | Auth Required |
| ------ | --------- | ---------------------------------------------- | ------------- |
| GET    | `/health` | Liveness check — returns `{"status": "ok"}`    | No            |
| GET    | `/ready`  | Readiness check — verifies DB connectivity     | No            |
