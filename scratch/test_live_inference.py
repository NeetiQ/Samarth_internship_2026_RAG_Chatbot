import sys
import os
from dotenv import load_dotenv

# Load root .env
load_dotenv("e:/Neetiq/legal-rag/.env")

# Append paths
sys.path.append("e:/Neetiq/legal-rag")
sys.path.append("e:/Neetiq/legal-rag/backend")

from retrieval.embeddings.embedder import Embedder

def main():
    print("Initializing production Embedder...")
    embedder = Embedder()
    
    test_query = "What is the scope of Section 319 CrPC?"
    print(f"Sending test query: '{test_query}'...")
    
    try:
        embedding = embedder.encode(test_query)
        print("Success! Received embedding response.")
        print(f"Vector Length: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        
        # Test batch encoding
        test_chunks = [
            "This is chunk number one of the document.",
            "This is chunk number two of the document."
        ]
        print(f"Sending batch text list: {test_chunks}...")
        embeddings = embedder.encode_batch(test_chunks)
        print("Success! Received batch embedding response.")
        print(f"Number of vectors: {len(embeddings)}")
        print(f"Vector 1 Length: {len(embeddings[0])}")
        print(f"Vector 2 Length: {len(embeddings[1])}")
        
    except Exception as e:
        print(f"Failed to query live embedding service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
