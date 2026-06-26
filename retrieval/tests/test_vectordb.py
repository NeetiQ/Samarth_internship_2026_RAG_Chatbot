"""
Test PGVector functionality.
"""

from retrieval.vectordb.pgvector_store import PGVectorStore


def main():

    PGVectorStore.create_table()

    print("✅ PGVector table verified successfully.")


if __name__ == "__main__":
    main()