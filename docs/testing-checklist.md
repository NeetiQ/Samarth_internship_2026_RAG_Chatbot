# Testing Checklist

**Last Updated**: 2026-07-06

---

## Backend API Tests (`legal-rag/backend/`)

### Authentication (`/api/v1/auth`)
- [ ] `POST /api/v1/auth/signup` — valid email and password
- [ ] `POST /api/v1/auth/signup` — duplicate email returns 400
- [ ] `POST /api/v1/auth/signup` — weak password validation
- [ ] `POST /api/v1/auth/login` — valid credentials returns JWT
- [ ] `POST /api/v1/auth/login` — invalid credentials returns 401
- [ ] `GET /api/v1/auth/me` — valid token returns user info
- [ ] `GET /api/v1/auth/me` — expired/invalid token returns 401

### Documents & Ingestion (`/api/v1/documents`)
- [ ] `POST /api/v1/documents/upload` — valid PDF file
- [ ] `POST /api/v1/documents/upload` — invalid file type rejected
- [ ] `POST /api/v1/documents/upload` — file too large rejected
- [ ] `POST /api/v1/documents/upload` — unauthenticated returns 401
- [ ] `GET /api/v1/documents` — returns document list
- [ ] `GET /api/v1/documents/{id}` — returns document details
- [ ] `GET /api/v1/documents/{id}/status` — returns processing job stage

### Retrieval (`/api/v1/retrieval`)
- [ ] `POST /api/v1/retrieval/retrieve` — valid query returns results
- [ ] `POST /api/v1/retrieval/retrieve` — empty query handled
- [ ] `POST /api/v1/retrieval/retrieve` — top_k parameter respected

### Chat (`/api/v1/chat`)
- [ ] `POST /api/v1/chat` — valid message with `use_rag=true`
- [ ] `POST /api/v1/chat` — valid message with `use_rag=false`
- [ ] `POST /api/v1/chat` — empty message handled
- [ ] `POST /api/v1/chat` — missing session_id creates new session
- [ ] `POST /api/v1/chat/history` — creates new session
- [ ] `GET /api/v1/chat/history/{session_id}` — returns messages
- [ ] `POST /api/v1/chat/query-rewrite` — rewrites query with history context

### System
- [ ] `GET /health` — returns 200 with `{"status": "ok"}`
- [ ] `GET /ready` — returns 200 when DB is connected
- [ ] `GET /ready` — returns 503 when DB is unreachable

### Schemas & Validation
- [ ] ChatRequest validation (Pydantic)
- [ ] ChatResponse serialization
- [ ] DocumentUpload validation
- [ ] RetrievalRequest validation
- [ ] Error responses follow `{"detail": "..."}` format

---

## Ingestion Pipeline Tests (`legal-rag/extracted/`, `legal-rag/chunking/`)

### PDF Extraction
- [ ] Extract text from valid PDF (PyMuPDF)
- [ ] Handle encrypted PDF gracefully
- [ ] Detect scanned PDF and trigger OCR
- [ ] Preserve page numbers in metadata

### Text Cleaning
- [ ] Normalize whitespace and encoding
- [ ] Handle special characters
- [ ] Remove headers/footers if configured

### Chunking
- [ ] Create chunks with configurable size (default: 600 tokens)
- [ ] Maintain configurable overlap (default: 100 tokens)
- [ ] Don't split mid-sentence
- [ ] Preserve chunk metadata (page_number, section, chunk_index)

### Pinecone Upload
- [ ] Upload vectors with metadata successfully
- [ ] Handle Pinecone API errors
- [ ] Batch upload large document sets

---

## Retrieval Pipeline Tests (`legal-rag/retrieval/`)

### Embeddings
- [ ] Generate embedding using `all-MiniLM-L6-v2` (384 dimensions)
- [ ] Handle empty text input
- [ ] Batch embedding processing

### Vector DB (Pinecone)
- [ ] Insert vectors with metadata
- [ ] Search by vector returns relevant results
- [ ] Filter results by metadata
- [ ] Handle Pinecone connection errors

### Search
- [ ] Semantic search returns ranked results
- [ ] Top-k parameter works correctly (default: 5)
- [ ] Query preprocessing applied

### Reranker
- [ ] Cross-encoder reranking improves relevance order
- [ ] Handle empty input gracefully
- [ ] Performance acceptable (< 500ms)

---

## Chat & RAG Tests (`legal-rag/rag_chat/`)

### LLM Integration (Gemini)
- [ ] Call Google Gemini API via `google-genai` SDK
- [ ] Handle API errors (rate limit, auth failure)
- [ ] Token counting works correctly

### Prompts
- [ ] System prompt renders correctly with legal domain context
- [ ] Chat history is formatted and injected
- [ ] Context from retrieval is properly included

### Citations
- [ ] Extract citations from Gemini output
- [ ] Validate citation references against retrieved chunks
- [ ] Handle missing sources gracefully

### RAG Pipeline
- [ ] Full pipeline: query → retrieval → context build → Gemini → response
- [ ] Chat history enables multi-turn conversations
- [ ] Retrieval connector properly calls retrieval service

---

## Frontend Tests (`legal-rag/frontend/`)

### Authentication
- [ ] Login form submits credentials
- [ ] Successful login redirects to `/dashboard`
- [ ] Failed login shows error message
- [ ] Signup form creates new account
- [ ] JWT token stored and sent with API requests
- [ ] Logout clears token and redirects to `/`

### Chat Page (`/chat`)
- [ ] Render user messages
- [ ] Render AI (assistant) responses
- [ ] Display citations/sources
- [ ] Send message via ChatInput
- [ ] Conversation list shows past sessions

### Dashboard (`/dashboard`)
- [ ] HeroCard displays correctly
- [ ] Navigate to chat via CTA button

### Upload Documents (`/upload-documents`)
- [ ] File upload UI works
- [ ] Display upload progress/status
- [ ] Show error messages for invalid files

### Settings (`/settings`)
- [ ] Theme toggle (dark/light mode) works
- [ ] Settings persist across page reloads

### Navigation
- [ ] Navbar links navigate correctly
- [ ] Responsive sidebar works on mobile
- [ ] Browser back/forward buttons work
- [ ] Direct URL navigation works (no 404)
- [ ] Page refresh works on all routes

---

## Integration Testing

### Backend ↔ Retrieval
- [ ] Ingest document → chunks created → searchable in Pinecone

### Retrieval ↔ Chat
- [ ] Search documents → results passed to Gemini → response generated with citations

### Frontend ↔ Backend
- [ ] Login → JWT received → authenticated API calls work
- [ ] Upload document → processing status updates
- [ ] Send chat message → RAG response displayed with citations

### Full E2E Pipeline
- [ ] Upload document (Frontend → Backend → Extraction → Chunking → Pinecone)
- [ ] Ask question (Frontend → Backend → Retrieval → Gemini → Response)
- [ ] View answer with citations (Frontend displays response + sources)

---

## Deployment Validation

### Frontend (Vercel)
- [ ] All routes load without 404 (`/`, `/login`, `/dashboard`, `/chat`, `/upload-documents`, `/compare`, `/settings`, `/signup`)
- [ ] Browser refresh works on all routes
- [ ] Deep links work (direct URL navigation)
- [ ] `vercel.json` SPA rewrites configured
- [ ] Environment variable `VITE_API_URL` set correctly

### Backend (Render)
- [ ] `GET /health` returns 200
- [ ] `GET /ready` returns 200
- [ ] CORS allows Vercel frontend URLs
- [ ] Database migrations applied
- [ ] Pinecone connection working

### Cross-Origin
- [ ] Frontend can call backend API without CORS errors
- [ ] Authentication flow works end-to-end in production

---

## Security Testing

### Authentication
- [ ] JWT token required for protected endpoints
- [ ] Expired token rejected
- [ ] Invalid token rejected
- [ ] Passwords hashed with bcrypt (passlib)

### Input Validation
- [ ] SQL injection prevented (SQLAlchemy parameterized queries)
- [ ] XSS prevented (React auto-escaping)
- [ ] File upload validation (type, size)

### CORS
- [ ] Only allowed origins can make requests
- [ ] Credentials properly handled

---

## Browser Compatibility

- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Edge (latest 2 versions)
- [ ] Responsive design on mobile devices
