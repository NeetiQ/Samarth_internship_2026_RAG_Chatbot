# Data Sources

## Supported File Formats

### Primary
- **PDF** (.pdf) — Text-based and scanned (OCR via PaddleOCR)
  - Extraction: PyMuPDF (`fitz`)
  - Fallback OCR: PaddleOCR for scanned/image-based PDFs

### File Size Limits
- Single file upload via Frontend UI
- Size limits configurable via backend settings

---

## Document Metadata

### Automatically Extracted

**From file system:**
- File name
- Upload date
- File size
- File type

**From content (via extraction pipeline):**
- Title / Heading
- Document type (contract, agreement, judgment, policy, etc.)
- Page numbers
- Section structure

### Structured Metadata (PostgreSQL)

Stored in the `documents` table:
- `court` — Court name
- `case_number` — Case identifier
- `judgment_date` — Date of judgment
- `source` — Document origin
- `language` — Document language

---

## Data Source Integration

### Frontend Upload

Via the Upload Documents page (`/upload-documents`):
- File selection interface
- Progress tracking
- Error handling for invalid files

### API Upload

```bash
curl -X POST https://legal-rag-backend-zf50.onrender.com/api/v1/documents/upload \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@contract.pdf"
```

---

## Data Processing Pipeline

### Ingestion Flow

```
1. File Upload (Frontend or API)
   ↓
2. File Validation (Backend)
   - Check format (PDF)
   - Store file reference
   ↓
3. PDF Extraction (extracted/pdf_extractor.py)
   - Text extraction via PyMuPDF
   - OCR fallback for scanned documents (PaddleOCR)
   ↓
4. Text Cleaning (extracted/text_cleaner.py)
   - Normalize whitespace and encoding
   - Remove artifacts
   ↓
5. Metadata Loading (extracted/metadata_loader.py)
   - Extract structured metadata
   ↓
6. Document Building (extracted/document_builder.py)
   - Assemble cleaned text with metadata
   ↓
7. Chunking (chunking/chunker.py)
   - LangChain text splitting
   - Configurable chunk size (default: 600 tokens)
   - Configurable overlap (default: 100 tokens)
   ↓
8. Embedding Generation
   - Sentence-Transformers (all-MiniLM-L6-v2, 384 dimensions)
   ↓
9. Vector Upload (ingestion/outputs/pinecone/)
   - Upload to Pinecone with metadata
   ↓
10. PostgreSQL Update
    - Document and chunk records created
    - Processing job status updated
```

---

## Vector Storage (Pinecone)

Each chunk is stored as a vector in Pinecone with metadata:

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

**Configuration:**
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Similarity metric: Cosine
- Index name: Configurable via `PINECONE_INDEX` env var

---

## Pre-loaded Corpus

The project includes a pre-processed legal document corpus:

- `chunked_documents_new.zip` — Pre-chunked legal documents
- `embedded_documents.jsonl` — Pre-computed embeddings (563 MB)

These can be seeded into Pinecone during initial deployment via the Docker Compose `SEED_CORPUS` environment variable.

---

## Data Quality Standards

### Text Extraction Accuracy
- **Text PDFs**: ≥ 99% accuracy expected
- **Scanned PDFs**: ≥ 90% accuracy expected (PaddleOCR)

### Chunk Quality
- **Completeness**: Each chunk includes full context
- **Coherence**: Chunks don't split mid-sentence (LangChain sentence-aware splitting)
- **Overlap**: Configurable overlap between chunks for context continuity
- **Metadata**: All chunks retain document references and page numbers

---

## Example Data

See `examples/` directory for:
- `sample_chunks.json` — Example chunked output
- `sample_retrieval.json` — Example search results
- `sample_chat_response.json` — Example LLM response
