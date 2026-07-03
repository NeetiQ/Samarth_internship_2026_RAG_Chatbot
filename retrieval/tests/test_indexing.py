from retrieval.pipelines.retrieval_service import RetrievalService

FILE_PATH = "chunked_documents.jsonl"


def main():

    service = RetrievalService()

    service.index_documents(FILE_PATH)


if __name__ == "__main__":
    main()