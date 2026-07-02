from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from embedding_config import *

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)

print("Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)

query = "What is anticipatory bail?"

print("Generating query embedding...")
embedding = model.encode(query).tolist()

print("Searching...")

results = index.query(
    vector=embedding,
    top_k=5,
    include_metadata=True
)

print("\nTop Results:\n")

for i, match in enumerate(results["matches"], start=1):

    metadata = match.get("metadata", {})

    print(f"Result {i}")
    print(f"Score        : {match['score']}")
    print(f"Case ID      : {metadata.get('case_id', 'N/A')}")
    print(f"Title        : {metadata.get('title', 'N/A')}")
    print(f"Court        : {metadata.get('court', 'N/A')}")
    print(f"Decision Date: {metadata.get('decision_date', 'N/A')}")
    print(f"Citation     : {metadata.get('citation', 'N/A')}")
    print(f"Judge        : {metadata.get('judge', 'N/A')}")
    print(f"Chunk ID     : {metadata.get('chunk_id', 'N/A')}")
    print(f"Source       : {metadata.get('source', 'N/A')}")

    print("\nText:")
    print(metadata.get("text", "")[:500])

    print("-" * 80)