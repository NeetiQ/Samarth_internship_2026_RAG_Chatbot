from retrieval.pipelines.retrieval_service import RetrievalService

# TODO:
# Replace this path with Team A's final repository path once available.
FILE_PATH = "chunked_documents.jsonl"


def main():

    service = RetrievalService()

    documents = service.ingest_documents(FILE_PATH)

    print(f"Total Chunks: {len(documents)}")
    print(f"Embedding Dimension: {len(documents[0]['embedding'])}")

    print("\nMetadata:")
    print(documents[0]["metadata"])


if __name__ == "__main__":
    main()