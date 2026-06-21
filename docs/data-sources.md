# Data Sources

TBD - Add data source documentation here.

2. **Word Documents**
   - .docx (Microsoft Word)
   - .doc (Legacy format)

3. **Text Files**
   - .txt (Plain text)
   - .md (Markdown)
   - .rtf (Rich text)

4. **Specialized Legal Formats**
   - .docm (Macro-enabled)
   - .xml (Structured legal XML)

### File Size Limits

- Single file: 100 MB
- Batch upload: 500 MB
- Daily ingestion: 5 GB (configurable)

## Document Metadata

### Automatically Extracted

From file system:
- File name
- Upload date
- File size
- File type

From content:
- Title/Heading
- Document type (contract, agreement, policy, etc.)
- Key dates (effective, expiration, amendment)
- Parties involved
- Document sections/structure

### User-Provided Metadata

Optional fields:
```json
{
  "case_id": "2024-ABC-123",
  "matter_number": "ABC-2024-001",
  "client_name": "Client Corp",
  "opposing_counsel": "Opposing Law Firm",
  "document_tags": ["confidential", "amended"],
  "importance_level": "high",
  "review_deadline": "2024-02-15"
}
```

## Data Source Integration

### Direct Upload

Via Frontend UI:
- Single file upload
- Batch upload (drag & drop)
- Progress tracking
- Error handling

### API Integration

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Authorization: Bearer <token>" \
  -F "file=@contract.pdf" \
  -F "document_type=contract"
```

### Bulk Import

```bash
# Script-based bulk import
python ingestion/scripts/bulk_import.py \
  --input-dir "./documents/" \
  --document-type "contract" \
  --batch-size 50
```

### Cloud Storage Integration

#### AWS S3

```python
# In ingestion/pdf_loader/s3_loader.py
import boto3

s3 = boto3.client('s3')
response = s3.list_objects_v2(
    Bucket='legal-documents',
    Prefix='contracts/'
)

for obj in response['Contents']:
    # Download and ingest
    doc = s3.get_object(
        Bucket='legal-documents',
        Key=obj['Key']
    )
```

#### Google Cloud Storage

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('legal-documents')
blobs = bucket.list_blobs(prefix='contracts/')

for blob in blobs:
    # Download and ingest
    blob.download_to_filename(blob.name)
```

#### Azure Blob Storage

```python
from azure.storage.blob import BlobServiceClient

client = BlobServiceClient.from_connection_string(
    "DefaultEndpointsProtocol=https;..."
)
container = client.get_container_client('legal-documents')

for blob in container.list_blobs(name_starts_with='contracts/'):
    # Download and ingest
    data = blob.download_blob().readall()
```

### Email Integration

```python
# Ingest documents from email attachments
import imaplib

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email, password)

_, messages = mail.search(None, 'UNSEEN')
for msg_id in messages[0].split():
    # Extract attachments
    # Ingest documents
```

### Database Integration

#### PostgreSQL Source

```python
# Ingest from existing legal documents table
import psycopg2

conn = psycopg2.connect("dbname=legacy_db ...")
cur = conn.cursor()

cur.execute(
    "SELECT document_id, content, metadata FROM documents"
)

for doc_id, content, metadata in cur.fetchall():
    # Process and ingest
```

#### Legal Document Management Systems

- LexisNexis
- Westlaw
- Thomson Reuters EDRM
- OpenText

## Data Processing Pipeline

### Ingestion Steps

```
1. File Upload/Import
   ↓
2. File Validation
   - Check format
   - Verify size
   - Scan for malware
   ↓
3. Storage
   - Save original file
   - Generate preview
   ↓
4. OCR (if scanned)
   - Extract text
   - Save OCR output
   ↓
5. Preprocessing
   - Clean text
   - Fix encoding
   - Normalize formatting
   ↓
6. Chunking
   - Split into chunks (1000 tokens)
   - Add overlap (200 tokens)
   - Maintain context
   ↓
7. Metadata Extraction
   - Entity recognition
   - Date extraction
   - Structure analysis
   ↓
8. Embedding Generation
   - Create vector embeddings
   - Store in vector DB
   ↓
9. Indexing
   - Update search indexes
   - Update metadata DB
   ↓
10. Notification
    - User confirmation
    - Process monitoring
```

## Data Quality Standards

### Text Extraction Accuracy

- **Text PDFs**: ≥ 99% accuracy expected
- **Scanned PDFs**: ≥ 90% accuracy expected
  - Uses fuzzy matching for OCR errors
  - Fallback: Flag sections for manual review

### Chunk Quality Metrics

- **Completeness**: Each chunk includes full context
- **Coherence**: Chunks don't split mid-sentence
- **Overlap**: 200 tokens overlap between chunks
- **Metadata**: All chunks have document references

### Metadata Accuracy

- **Auto-extracted**: Validated against content
- **User-provided**: Checked for consistency
- **Temporal**: Date validation and normalization

## Retention & Archival

### Retention Policies

```
Active Documents:
- Keep full versions
- Keep embeddings
- Keep metadata
- Duration: Indefinite or per policy

Archived Documents:
- Keep metadata only
- Archive embeddings (compressed)
- Keep original file (cold storage)
- Duration: 7 years (typical legal requirement)

Deleted Documents:
- Remove from vector DB
- Remove from embeddings
- Keep audit log
- Secure deletion (3-pass overwrite)
```

### Export Formats

Users can export:
- Original documents
- Extracted text
- Processed chunks
- Metadata (CSV/JSON)
- Search results
- Chat transcripts

### GDPR/Privacy Compliance

- [ ] Data anonymization options
- [ ] Right to deletion implementation
- [ ] Data portability export
- [ ] Consent tracking
- [ ] Processing agreement documentation

## Monitoring Data Sources

### Health Checks

```bash
# Check ingestion queue
curl http://localhost:8000/api/ingest/queue

# Check document statistics
curl http://localhost:8000/api/documents/stats
```

### Metrics to Track

- Documents ingested (daily/weekly/monthly)
- Average ingestion time
- OCR accuracy rate
- Chunk quality metrics
- Storage utilization
- Error rates by document type

## Troubleshooting

### Common Issues

**Problem**: PDF extraction failing
- Check: File is not encrypted
- Check: PDF is not image-based (needs OCR)
- Solution: Enable OCR pipeline

**Problem**: Low OCR accuracy
- Check: Document quality (resolution ≥ 300 DPI)
- Check: Language settings
- Solution: Manual verification, use better OCR model

**Problem**: Metadata extraction errors
- Check: Document structure (not corrupted)
- Solution: Manual metadata entry

**Problem**: Duplicate documents detected
- Check: File hash (content-based deduplication)
- Solution: Skip or merge duplicates

## Example Data

See `examples/` directory for:
- `sample_chunks.json` - Example chunked output
- `sample_retrieval.json` - Example search results
- `sample_chat_response.json` - Example LLM response
