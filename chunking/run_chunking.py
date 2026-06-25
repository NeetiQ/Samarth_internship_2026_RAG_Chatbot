from chunker import DocumentChunker

from config import (
    INPUT_FILE,
    OUTPUT_FILE
)


def main():

    chunker = DocumentChunker()

    documents = chunker.load_documents(
        INPUT_FILE
    )

    chunked_documents = (
        chunker.chunk_documents(
            documents
        )
    )

    chunker.save_chunks(
        chunked_documents,
        OUTPUT_FILE
    )

    print(
        f"Chunking completed. "
        f"Output saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()