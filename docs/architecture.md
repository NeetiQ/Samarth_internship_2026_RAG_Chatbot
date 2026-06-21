# Architecture Overview

TBD - Add system architecture and design documentation here.

## Component Architecture

### 1. Ingestion Pipeline (Team A: legal-rag/ingestion/)

**Purpose**: Convert raw legal documents into searchable chunks with metadata.

**Flow**:
```
PDF/Document → PDF Loader → OCR (if needed) → Preprocessing → 
Chunking → Metadata Extraction → Vector DB
```

**Components**:
- `pdf_loader/`: Handles PDF extraction and text parsing
- `ocr/`: Pytesseract/PaddleOCR for scanned documents
- `preprocessing/`: Normalization, cleaning, entity extraction
- `chunking/`: Intelligent splitting with overlap strategy
- `metadata/`: Extract case info, dates, parties, document type

**Output**: 
- Chunks stored in `outputs/chunks/` (JSON)
- Metadata stored in `outputs/metadata/` (JSON/CSV)

### 2. Retrieval Pipeline (Team B: legal-rag/retrieval/)

**Purpose**: Enable semantic search over ingested documents.

**Flow**:
```
User Query → Query Embedding → Vector Search → 
Reranking → Retrieved Documents → Return to Chat
```

**Components**:
- `embeddings/`: Generate embeddings (OpenAI, Sentence-Transformers)
- `vectordb/`: Manage vector storage (Pinecone, Milvus, Weaviate)
- `search/`: BM25 + semantic search hybrid approach
- `reranker/`: Cross-encoder reranking for relevance
- `pipelines/`: Orchestrate search workflows

### 3. Chat & Reasoning (Team C: legal-rag/rag_chat/)

**Purpose**: Generate accurate, cited responses using LLM + retrieved context.

**Flow**:
```
Retrieved Documents + Query → Prompt Engineering → 
LLM Generation → Citation Extraction → Response
```

**Components**:
- `llm/`: LLM interface (OpenAI, Anthropic, HuggingFace)
- `prompts/`: System prompts, few-shot examples, templates
- `citations/`: Extract and format source citations
- `workflows/`: Multi-turn conversation state management

### 4. Frontend (Team D: legal-rag/frontend/)

**Purpose**: User interface for document upload and chat.

**Structure**:
```
App
├── Components
│   ├── Chat: Message display, input, streaming
│   ├── Upload: Document drop zone, progress
│   ├── Citations: Display retrieved sources
│   ├── Dashboard: Stats, document list
│   └── Common: Header, layout, utilities
├── Hooks: Custom hooks for API calls, state
├── Services: API client, authentication
└── Styles: Global styles, themes
```

### 5. Backend API (legal-rag/backend/)

**Purpose**: REST API orchestrating all operations.

**Endpoints**:
- `POST /api/chat`: Send message, get response
- `POST /api/ingest`: Upload and process document
- `GET /api/retrieval`: Search documents
- `GET /health`: Health check

**Structure**:
```
app/
├── main.py: FastAPI app initialization
├── api/: Route handlers
├── schemas/: Pydantic models for validation
├── services/: Business logic
├── core/: Config, logging, database
└── tests/: Unit and integration tests
```

### 6. Deployment (Team E: legal-rag/deployment/)

**Purpose**: Containerization and infrastructure.

**Components**:
- `docker/`: Dockerfiles for backend, frontend
- `scripts/`: Deployment automation scripts
- `github-actions/`: CI/CD pipelines
- `monitoring/`: Prometheus metrics, health checks

### 7. Shared Utilities (legal-rag/shared/)

**Purpose**: Common code used across teams.

**Components**:
- `configs/`: Shared configuration models
- `constants/`: Application constants
- `utils/`: Helper functions
- `models/`: Shared data models

## Data Flow

### Document Ingestion Flow

```
1. User uploads PDF via Frontend
   ↓
2. Backend receives file, stores temporarily
   ↓
3. Ingestion Pipeline processes:
   - PDF extraction
   - Text normalization
   - Document chunking (1000 tokens, 200 overlap)
   - Metadata extraction
   ↓
4. Embeddings generated for each chunk
   ↓
5. Chunks + embeddings stored in Vector DB
   ↓
6. Metadata stored in PostgreSQL
   ↓
7. Frontend shows success, updates document list
```

### Query/Response Flow

```
1. User asks question in chat
   ↓
2. Query encoded to embedding
   ↓
3. Semantic search in Vector DB (top-k=5)
   ↓
4. Retrieved chunks reranked for relevance
   ↓
5. Top chunks + system prompt sent to LLM
   ↓
6. LLM generates response with citations
   ↓
7. Citations resolved to source documents
   ↓
8. Response + citations sent to Frontend
   ↓
9. Frontend displays message + source links
```

## Database Schema

### PostgreSQL (Metadata)

```sql
-- Documents
documents (id, filename, upload_date, file_size, document_type)

-- Chunks
chunks (id, document_id, chunk_index, text, page_number, created_at)

-- Metadata
metadata (chunk_id, key, value)

-- Chat History
conversations (id, user_id, created_at, updated_at)
messages (id, conversation_id, role, content, created_at)
```

### Vector DB (Pinecone/Milvus)

```json
{
  "id": "chunk_12345",
  "values": [0.123, 0.456, ...],  // embedding vector
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

## Technology Stack

| Layer      | Technology                              |
| ---------- | --------------------------------------- |
| Frontend   | React/Next.js, TypeScript, Tailwind CSS |
| Backend    | Python, FastAPI, Pydantic               |
| Database   | PostgreSQL (metadata), Redis (cache)    |
| Vector DB  | Pinecone / Milvus                       |
| Embeddings | OpenAI text-embedding-3-small           |
| LLM        | GPT-4, Claude 3, LLaMA                  |
| Containers | Docker, Docker Compose                  |
| CI/CD      | GitHub Actions                          |

## Security Considerations

1. **API Authentication**: JWT tokens for API access
2. **Data Encryption**: TLS for transit, encryption at rest
3. **Access Control**: Role-based access (admin, user, viewer)
4. **Rate Limiting**: API rate limits per user/key
5. **Audit Logging**: All operations logged and timestamped
6. **PII Masking**: Sensitive data redaction options

## Scalability & Performance

- **Horizontal Scaling**: Stateless backend services in Kubernetes
- **Caching**: Redis for query results and session data
- **Batch Processing**: Async ingestion for large documents
- **Vector DB Optimization**: Dimensionality reduction, indexing strategies
- **CDN**: Static assets served via CDN

## Monitoring & Observability

- **Metrics**: Prometheus for system metrics
- **Logging**: JSON structured logs to ELK or CloudWatch
- **Tracing**: OpenTelemetry for request tracing
- **Alerts**: PagerDuty integration for critical issues
