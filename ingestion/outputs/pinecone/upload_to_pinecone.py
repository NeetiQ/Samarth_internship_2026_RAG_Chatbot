import json
import uuid

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from embedding_config import *

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("✅ Model loaded.")

print("Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
print("✅ Connected to Pinecone.")

print("Opening chunked_documents_new.jsonl...")

batch = []
count = 0

with open("chunked_documents_new.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        chunk = json.loads(line)

        text = chunk["page_content"]

        embedding = model.encode(text).tolist()

        metadata = chunk.get("metadata", {})

        batch.append(
            {
                "id": metadata.get("chunk_id", str(uuid.uuid4())),
                "values": embedding,
                "metadata": {
                    "text": text,
                    "chunk_id": metadata.get("chunk_id", ""),
                    "source": metadata.get("source", ""),
                    "title": metadata.get("title", ""),
                    "case_id": metadata.get("case_id", ""),
                    "court": metadata.get("court", ""),
                    "decision_date": metadata.get("decision_date", ""),
                    "citation": metadata.get("citation", ""),
                    "judge": metadata.get("judge", ""),
                    "year": metadata.get("year", "")
                },
            }
        )

        count += 1

        if count % 500 == 0:
            print(f"Processed {count} chunks...")

        if len(batch) == 500:
            index.upsert(vectors=batch)
            batch = []

if batch:
    index.upsert(vectors=batch)
    print(f"✅ Uploaded final {len(batch)} chunks.")

print(f"✅ Upload completed. Total chunks uploaded: {count}")