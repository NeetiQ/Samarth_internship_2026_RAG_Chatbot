from retrieval.vectordb.pgvector_store import PGVectorStore


def main():
    PGVectorStore.create_table()


if __name__ == "__main__":
    main()