import sys
import os
from dotenv import load_dotenv

# Load root .env
load_dotenv("e:/Neetiq/legal-rag/.env")

# Append paths
sys.path.append("e:/Neetiq/legal-rag")
sys.path.append("e:/Neetiq/legal-rag/backend")

def test_client_imports():
    print("Testing client imports...")
    try:
        from retrieval.embeddings.client import EmbeddingClient
        client = EmbeddingClient()
        print("EmbeddingClient imported successfully.")
        print(f"Service URL: {client.url}")
        print(f"API Key present: {bool(client.api_key)}")
    except Exception as e:
        print(f"Failed to import/init EmbeddingClient: {e}")
        sys.exit(1)

def test_embedder_imports():
    print("Testing embedder imports...")
    try:
        from retrieval.embeddings.embedder import Embedder
        embedder = Embedder()
        print("Embedder imported successfully.")
    except Exception as e:
        print(f"Failed to import/init Embedder: {e}")
        sys.exit(1)

def test_no_sentence_transformer():
    print("Verifying sentence_transformers is NOT imported by model.py...")
    try:
        from retrieval.embeddings.model import EmbeddingModel
        try:
            EmbeddingModel.get_model()
            print("ERROR: get_model() did not raise an error!")
            sys.exit(1)
        except RuntimeError as re:
            print(f"Success: get_model() correctly blocked: {re}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_client_imports()
    test_embedder_imports()
    test_no_sentence_transformer()
    print("All local import & configuration validations PASSED.")
