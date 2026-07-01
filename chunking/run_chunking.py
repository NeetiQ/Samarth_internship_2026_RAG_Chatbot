from chunker import DocumentChunker
from config import INPUT_FILE, OUTPUT_FILE


def main():

    chunker = DocumentChunker()

    documents = chunker.load_documents(
        INPUT_FILE
    )

    chunked_documents = chunker.chunk_documents(
        documents
    )

    chunker.save_chunks(
        chunked_documents,
        OUTPUT_FILE
    )

    print("\n" + "=" * 60)
    print("Chunking Completed Successfully")
    print("=" * 60)
    print(f"Original Documents : {len(documents)}")
    print(f"Generated Chunks   : {len(chunked_documents)}")
    print(f"Output File        : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()