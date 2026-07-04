# RAG Pipeline

> **Basis:** This document is grounded directly in the source Architecture & Workflows specification (ingestion, retrieval, and chat sub-workflows). Chunking parameters, sub-workflow steps, and cross-module dependencies are taken from that document. The "why" explanations are added for clarity; ownership-scoping notes in the retrieval section are **PROPOSED DESIGN**.

## Part 1 — Ingestion Pipeline

```mermaid
graph TD
    A[PDF Upload] --> B[OCR / Text Extraction]
    B --> C[Metadata Extraction]
    C --> D[Cleaning]
    D --> E[Chunking]
    E --> F[Embedding Generation]
    F --> G[Vector Storage - PGVector]
    G --> H[Processing Job Marked Complete]
    H --> I[Search Ready]
```

| Stage | What it does | Why it exists |
|---|---|---|
| PDF Upload | Accepts the file, assigns a document ID | Establishes a stable identity for tracking status through every later stage |
| OCR / Text Extraction | Reads raw text and structure from the PDF | Legal PDFs are often scanned or mixed-layout; without OCR, text-layer extraction alone would miss content |
| Metadata Extraction | Captures source, page numbers, title, etc. | This is the data citations are built from later — losing it here means answers can't be traced back to a source |
| Cleaning | Normalizes whitespace, removes OCR artifacts/noise | Embedding quality degrades on noisy text; clean input produces more reliable similarity search |
| Chunking | Splits cleaned text into fixed-size segments | A recursive character text splitter breaks documents into **1000-character chunks with 200-character overlap** — small enough for precise retrieval, with overlap to avoid severing context across chunk boundaries |
| Embedding Generation | Converts each chunk into a dense vector via `BAAI/bge-small-en-v1.5` | This is what makes semantic (not just keyword) search possible |
| Vector Storage | Writes vectors + metadata into PGVector | Makes chunks searchable via cosine similarity |
| Processing Job | Tracks status (`uploaded` → `extracting` → `chunked` → `processed` → `failed`) | Gives the frontend and API consumers visibility into long-running async processing |

**Source-specified intermediate outputs.** The original pipeline design persists intermediate state as JSONL files at each stage (`documents.jsonl` after extraction, `chunked_documents.jsonl` after chunking) before final vector storage. This provides a debug/replay trail if a later stage fails, so the pipeline can resume from the last successful stage rather than re-running OCR.

## Part 2 — Retrieval Pipeline

```mermaid
graph TD
    Q[User Query] --> QE[Query Embedding]
    QE --> SS[Similarity Search - PGVector Cosine]
    SS --> TK[Top-K Retrieval]
    TK --> MC[Metadata Collection]
```

The retrieval module generates a real-time embedding for the incoming query, connects to the PostgreSQL/PGVector store, and runs a cosine similarity lookup to fetch the Top-K most relevant chunks, returning them with their metadata (source, page, chunk ID) for the chat layer to consume.

> **📋 PROPOSED DESIGN — retrieval scope.** The source spec does not scope retrieval by user. To support the ownership model described in [DATABASE_DESIGN.md](./DATABASE_DESIGN.md), the similarity search is scoped to **the shared legal corpus plus the current user's own uploaded documents only** — never another user's private documents. See [SECURITY.md](./SECURITY.md) for enforcement details.

## Part 3 — RAG Chat Pipeline

```mermaid
graph TD
    Q[Question] --> E[Embedding]
    E --> S[Similarity Search]
    S --> T[Top-K Retrieval]
    T --> M[Metadata Collection]
    M --> P[Prompt Construction]
    P --> C[Conversation Context]
    C --> GM[Gemini]
    GM --> CI[Citation Engine]
    CI --> F[Final Response]
```

| Stage | Detail |
|---|---|
| Question | Raw user query received via `POST /api/v1/chat` |
| Embedding | Query is embedded with the same model used for chunk embeddings, so both live in the same vector space |
| Similarity Search / Top-K Retrieval | Handled by the retrieval module (Part 2) |
| Metadata Collection | Source, page number, and chunk ID are pulled from each retrieved chunk — required for citations |
| Prompt Construction | Combines the question, retrieved chunks, their metadata, and (if present) prior conversation history into a single instruction-formatted prompt for Gemini |
| Conversation Context | For multi-turn sessions, prior turns are gathered and folded into the prompt so follow-up questions resolve correctly |
| Gemini | Generates the natural-language answer grounded in the supplied context |
| Citation Engine | Maps statements in the response back to source file + page number, producing inline citations |
| Final Response | Answer + citations returned to the frontend |

### Query Rewriting

The chat module optionally rewrites follow-up queries using conversation history before retrieval — e.g., "what about clause 3?" is rewritten into a self-contained query using prior context, improving retrieval accuracy for conversational fragments.

## Related Documents

- [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) — where this pipeline sits in the overall system
- [DATABASE_DESIGN.md](./DATABASE_DESIGN.md) — how documents, chunks, and jobs are modeled
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) — endpoint reference for each stage
