# Team Deliverables

**Last Updated**: 2026-07-06

---

## Team A: Ingestion & Extraction Pipeline

### Deliverables

1. **PDF Extraction Module** (`extracted/`)
   - [x] PDF text extraction (PyMuPDF)
   - [x] Text cleaning and normalization
   - [x] Document builder and metadata loader
   - [x] Full extraction pipeline orchestration

2. **Chunking Module** (`chunking/`)
   - [x] Configurable chunk size (default: 600 tokens)
   - [x] Configurable overlap (default: 100 tokens)
   - [x] LangChain text splitter integration
   - [x] Run chunking pipeline script

3. **Pinecone Upload** (`ingestion/outputs/pinecone/`)
   - [x] Vector upload to Pinecone
   - [x] Embedding configuration
   - [x] Search testing utility
   - [x] Index health check

### Integration Points
- Outputs vectors to Pinecone vector database
- Stores document metadata in PostgreSQL via Backend API

---

## Team B: Retrieval Pipeline

### Deliverables

1. **Embeddings Module** (`retrieval/embeddings/`)
   - [x] Sentence-Transformers integration (`all-MiniLM-L6-v2`)
   - [x] 384-dimension embedding generation
   - [x] Configurable model selection

2. **Vector Database Module** (`retrieval/vectordb/`)
   - [x] Pinecone client wrapper (`pinecone_store.py`)
   - [x] Vector CRUD operations
   - [x] Metadata filtering support

3. **Semantic Search** (`retrieval/search/`)
   - [x] Vector similarity search via retriever
   - [x] Configurable top-k (default: 5)

4. **Reranking Module** (`retrieval/reranker/`)
   - [x] Cross-encoder reranking for relevance

5. **Retrieval Pipeline** (`retrieval/pipelines/`)
   - [x] End-to-end retrieval service
   - [x] Query → Embed → Search → Rerank → Results

### Integration Points
- Consumes query from Chat module
- Searches Pinecone for relevant chunks
- Returns ranked results to RAG pipeline

---

## Team C: RAG Chat & LLM

### Deliverables

1. **LLM Integration** (`rag_chat/llm/`)
   - [x] Google Gemini client via `google-genai` SDK
   - [x] Configurable model settings

2. **Prompt Engineering** (`rag_chat/prompts/`)
   - [x] System prompt for legal domain
   - [x] Chat history formatter

3. **Citation Module** (`rag_chat/citations/`)
   - [x] Citation extraction from LLM output
   - [x] Metadata parser for source references
   - [x] Citation formatting

4. **Conversation Workflows** (`rag_chat/workflows/`)
   - [x] RAG pipeline orchestration
   - [x] Context builder from retrieved chunks
   - [x] Retrieval connector to Team B's service
   - [x] Chat history support (configurable via env)

5. **Tests** (`rag_chat/tests/`)
   - [x] Test RAG pipeline
   - [x] Test citation formatter
   - [x] Test context builder
   - [x] Test Gemini client
   - [x] Test metadata parser
   - [x] Test prompt builder
   - [x] Test retrieval connector

### Integration Points
- Consumes retrieved documents from Retrieval Pipeline
- Calls Google Gemini for response generation
- Returns cited responses to Backend API

---

## Team D: Frontend

### Deliverables

1. **Authentication Pages**
   - [x] Login page (`/`) with JWT auth
   - [x] Signup page (`/signup`) with registration flow
   - [x] AuthContext for token management

2. **Chat Component** (`frontend/src/components/chat/`)
   - [x] ChatWindow with message display
   - [x] ChatInput for user message entry
   - [x] ChatHeader
   - [x] MessageBubble for user/assistant messages
   - [x] ConversationList for session management

3. **Dashboard** (`frontend/src/pages/Dashboard.jsx`)
   - [x] HeroCard with navigation to chat
   - [x] Dashboard layout

4. **Document Upload** (`frontend/src/pages/UploadDocuments.jsx`)
   - [x] File upload interface
   - [x] Progress/status display

5. **Settings** (`frontend/src/pages/Settings.jsx`)
   - [x] Theme toggle (dark/light mode)
   - [x] User preferences

6. **Navigation** (`frontend/src/components/layout/Navbar.jsx`)
   - [x] Responsive sidebar navigation
   - [x] Mobile-friendly layout
   - [x] Logout functionality

7. **API Integration** (`frontend/services/api.js`, `frontend/src/services/api.js`)
   - [x] Axios-based API client
   - [x] `VITE_API_URL` environment variable
   - [x] Authentication token handling

8. **Deployment Configuration**
   - [x] `vercel.json` for SPA routing
   - [x] Dockerfile + Nginx for Docker deployment
   - [x] `.dockerignore` for optimized builds
   - [x] Production Nginx config with security headers and caching

### Integration Points
- Calls Backend API via Axios (`VITE_API_URL`)
- JWT-based authentication
- Deployed on Vercel with auto-deploy from `main` branch

---

## Team E: Backend & Deployment

### Deliverables

1. **Backend API** (`backend/`)
   - [x] FastAPI application factory (`main.py`)
   - [x] Authentication endpoints (`/api/v1/auth`)
   - [x] Document endpoints (`/api/v1/documents`)
   - [x] Extraction endpoints (`/api/v1/extraction`)
   - [x] Retrieval endpoints (`/api/v1/retrieval`)
   - [x] Chat endpoints (`/api/v1/chat`)
   - [x] Health and readiness endpoints
   - [x] CORS configuration for Vercel origins
   - [x] Custom exception handlers

2. **Database** (`backend/alembic/`)
   - [x] SQLAlchemy ORM models
   - [x] Alembic migration management
   - [x] PostgreSQL on Render (managed)

3. **Vector DB Integration** (`backend/app/services/vector/`)
   - [x] Pinecone service wrapper

4. **Docker Setup**
   - [x] Backend Dockerfile
   - [x] Frontend Dockerfile (multi-stage: Node → Nginx)
   - [x] Docker Compose for local full-stack development
   - [x] Nginx configuration with security headers

5. **Cloud Deployment**
   - [x] Backend deployed on Render
   - [x] Frontend deployed on Vercel
   - [x] PostgreSQL managed on Render
   - [x] Pinecone cloud for vector storage

### Integration Points
- Orchestrates all pipeline modules
- Manages database lifecycle
- Handles authentication and authorization

---

## Cross-Team Dependencies

```
Team A (Extraction/Chunking)
    ↓ (outputs vectors to Pinecone)
Team B (Retrieval) ← Team D (Frontend triggers search via API)
    ↓ (returns relevant chunks)
Team C (RAG Chat + Gemini)
    ↓ (generates cited response)
Team E (Backend API)
    ↓ (serves response to client)
Team D (Frontend displays)
```

---

## Deployment URLs

| Component | URL |
| --------- | --- |
| Frontend  | https://samarth-internship-2026-rag-chatbot.vercel.app |
| Backend   | https://legal-rag-backend-zf50.onrender.com |
| API Docs  | https://legal-rag-backend-zf50.onrender.com/api/v1/docs |
