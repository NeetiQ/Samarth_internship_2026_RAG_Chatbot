# Testing Checklist

TBD - Add testing checklist and QA procedures here.

#### API Routes
- [ ] `POST /api/chat` - valid message
- [ ] `POST /api/chat` - empty message
- [ ] `POST /api/chat` - missing conversation_id
- [ ] `GET /health` - returns 200
- [ ] `GET /health` - checks all services
- [ ] `POST /api/ingest` - valid file
- [ ] `POST /api/ingest` - invalid file type
- [ ] `POST /api/ingest` - file too large

#### Schemas
- [ ] ChatRequest validation
- [ ] ChatResponse serialization
- [ ] IngestRequest validation
- [ ] RetrievalResponse serialization
- [ ] Error response format

#### Services
- [ ] Chat service with mocked LLM
- [ ] Ingest service with mocked storage
- [ ] Retrieval service with mocked vector DB

### Ingestion (legal-rag/ingestion/tests/)

#### PDF Loader
- [ ] Extract text from valid PDF
- [ ] Handle encrypted PDF
- [ ] Detect scanned PDF
- [ ] Preserve page numbers
- [ ] Extract metadata

#### OCR
- [ ] Pytesseract integration
- [ ] Language detection
- [ ] Image preprocessing
- [ ] Confidence scoring

#### Preprocessing
- [ ] Text normalization
- [ ] Entity extraction (dates)
- [ ] Entity extraction (parties)
- [ ] Handle special characters

#### Chunking
- [ ] Create chunks of ~1000 tokens
- [ ] Maintain 200 token overlap
- [ ] Don't split mid-sentence
- [ ] Preserve metadata

#### Metadata
- [ ] Extract key dates
- [ ] Identify parties
- [ ] Classify document type
- [ ] Extract section headers

### Retrieval (legal-rag/retrieval/tests/)

#### Embeddings
- [ ] Generate embedding for text
- [ ] Handle empty text
- [ ] Batch processing
- [ ] Caching mechanism

#### Vector DB
- [ ] Insert vector with metadata
- [ ] Search by vector
- [ ] Filter results
- [ ] Update existing vectors
- [ ] Delete vectors

#### Search
- [ ] Semantic search returns results
- [ ] BM25 search returns results
- [ ] Hybrid search combines both
- [ ] Query preprocessing

#### Reranker
- [ ] Rerank results by relevance
- [ ] Handle empty input
- [ ] Performance acceptable (< 500ms)

### Chat (legal-rag/rag_chat/tests/)

#### LLM Integration
- [ ] Call OpenAI API
- [ ] Handle API errors
- [ ] Token counting
- [ ] Stream responses

#### Prompts
- [ ] System prompt rendering
- [ ] Context injection
- [ ] Token limit enforcement
- [ ] Few-shot example formatting

#### Citations
- [ ] Extract citations from LLM output
- [ ] Validate citation references
- [ ] Format citations (APA, Chicago)
- [ ] Handle missing sources

### Frontend (legal-rag/frontend/)

#### Chat Component
- [ ] Render user message
- [ ] Render AI response
- [ ] Display citations
- [ ] Handle streaming

#### Upload Component
- [ ] Drag & drop file
- [ ] Select file via dialog
- [ ] Display upload progress
- [ ] Show error messages

#### API Integration
- [ ] Call POST /api/chat
- [ ] Handle authentication
- [ ] Retry on failure
- [ ] Timeout handling

## Integration Testing

### Backend-Retrieval Integration
- [ ] Ingest document → chunks created → searchable

### Retrieval-Chat Integration
- [ ] Search documents → results passed to LLM → response generated

### Chat-Frontend Integration
- [ ] User question in UI → API call → response displayed → citations linked

### Full Pipeline (E2E)
- [ ] Upload document (Frontend → Backend → Ingestion)
- [ ] Ask question (Frontend → Backend → Retrieval → Chat)
- [ ] View answer with citations (Frontend displays response)

## Performance Testing

### Load Testing

```bash
# Test backend with concurrent requests
# Expected: 100+ requests/second, p99 < 1000ms
ab -n 10000 -c 100 http://localhost:8000/api/health
```

### Search Latency

```
- Embedding generation: < 100ms
- Vector search: < 200ms
- Reranking: < 300ms
- Total retrieval: < 500ms
```

### Ingestion Speed

```
- PDF parsing: 1-5 seconds (depending on size)
- OCR (if needed): 5-30 seconds per page
- Chunking: < 100ms per document
- Embedding: 100-500ms per chunk
- Total: < 5 minutes for average document
```

### Memory Usage

```
- Backend service: < 500MB
- Frontend service: < 300MB
- Batch processing: < 2GB
```

## Security Testing

### Authentication
- [ ] JWT token required for protected endpoints
- [ ] Expired token rejected
- [ ] Invalid token rejected
- [ ] Token refresh works

### Authorization
- [ ] User can only access own documents
- [ ] Admin has elevated permissions
- [ ] Read-only users cannot upload

### Input Validation
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] File upload malware scan
- [ ] XXE prevention

### Data Protection
- [ ] Passwords hashed (bcrypt)
- [ ] Sensitive data encrypted
- [ ] TLS for transit
- [ ] No sensitive data in logs

## Compatibility Testing

### Browser Compatibility
- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Edge (latest 2 versions)

### Python Versions
- [ ] Python 3.9
- [ ] Python 3.10
- [ ] Python 3.11
- [ ] Python 3.12

### Operating Systems
- [ ] Windows 10/11
- [ ] macOS 12+
- [ ] Linux (Ubuntu 20.04+)

### Mobile
- [ ] Responsive design works
- [ ] Touch interactions work
- [ ] Slow networks handled

## Regression Testing

### Critical Paths
- [ ] Document upload still works
- [ ] Search still returns results
- [ ] Chat responses still generated
- [ ] Citations still extracted

### Before Each Release
- [ ] Run full test suite
- [ ] Manual smoke testing
- [ ] Performance benchmarks
- [ ] Security scan

## User Acceptance Testing (UAT)

### Functional Requirements

**Ingestion**
- [ ] Upload PDF document
- [ ] Upload Word document
- [ ] Upload multiple files
- [ ] See upload progress
- [ ] Receive completion notification

**Search**
- [ ] Search by keywords
- [ ] See results with relevance scores
- [ ] Filter by document type
- [ ] Sort results

**Chat**
- [ ] Ask question about documents
- [ ] See streaming response
- [ ] See citations with sources
- [ ] Click citation to view source

**Dashboard**
- [ ] See uploaded documents
- [ ] See usage statistics
- [ ] Download documents
- [ ] Delete documents

### Non-Functional Requirements

**Performance**
- [ ] Search completes in < 1 second
- [ ] Chat response starts streaming in < 2 seconds
- [ ] Upload shows smooth progress

**Usability**
- [ ] Interface is intuitive
- [ ] Error messages are clear
- [ ] Help text is available

**Accessibility**
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast adequate
- [ ] Text sizes readable

## Test Data

### Test Documents

```
examples/
├── sample_chunks.json          # 100 sample chunks
├── sample_retrieval.json       # 10 retrieval results
├── sample_chat_response.json   # 5 sample responses
├── test_documents/
│   ├── contract_sample.pdf
│   ├── agreement_sample.pdf
│   └── policy_sample.pdf
```

### Test Users

```
dev@example.com     - Developer account
tester@example.com  - QA account
admin@example.com   - Admin account
```

## Continuous Integration

### Pre-Commit Hooks

```bash
- Run linters (black, isort, flake8)
- Run type checking (mypy)
- Run unit tests
- Check code coverage
```

### CI Pipeline

```yaml
# .github/workflows/tests.yml
- Run all unit tests
- Generate coverage report
- Run integration tests
- Performance benchmarks
- Security scanning
- Build Docker images
```

### Coverage Requirements

- Backend: ≥ 80%
- Ingestion: ≥ 80%
- Retrieval: ≥ 80%
- Chat: ≥ 80%
- Overall: ≥ 80%

## Defect Tracking

Report bugs with:
- [ ] Description of issue
- [ ] Steps to reproduce
- [ ] Expected behavior
- [ ] Actual behavior
- [ ] Screenshots/logs
- [ ] Environment info
- [ ] Severity level

## Sign-Off

| Role               | Name | Date | Notes |
| ------------------ | ---- | ---- | ----- |
| QA Lead            |      |      |       |
| Dev Lead           |      |      |       |
| Product Manager    |      |      |       |
| Client Stakeholder |      |      |       |

---

**Last Updated**: 2024-01-15
**Next Review**: 2024-02-15
