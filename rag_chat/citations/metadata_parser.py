def parse_metadata(chunk):
    return {
        "doc_id": chunk.get("doc_id"),
        "source": chunk.get("source"),
        "page": chunk.get("page"),
        "chunk_id": chunk.get("chunk_id"),
        "chunk_number": chunk.get("chunk_number"),
        "total_chunks": chunk.get("total_chunks"),
        "ingestion_date": chunk.get("ingestion_date"),
        "document_type": chunk.get("document_type")
    }

def validate_metadata(metadata):
    required_fields = [
        "doc_id",
        "source",
        "page",
        "chunk_id"
    ]

    return all(metadata.get(field) is not None for field in required_fields)