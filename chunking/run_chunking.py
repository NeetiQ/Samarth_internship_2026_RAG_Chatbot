from chunking.chunker import DocumentChunker


def run_chunking(input_file: str, output_file: str):
    """
    Run the chunking pipeline.
    """

    chunker = DocumentChunker()

    print("Loading extracted documents...")

    documents = chunker.load_documents(input_file)

    print(f"Loaded {len(documents)} documents")

    print("Generating chunks...")

    chunked_documents = chunker.chunk_documents(documents)

    print(f"Generated {len(chunked_documents)} chunks")

    print("Saving chunks...")

    chunker.save_chunks(
        chunked_documents,
        output_file
    )

    print("Chunking completed successfully.")

    return {
        "status": "success",
        "documents": len(documents),
        "chunks": len(chunked_documents),
        "output_file": output_file,
    }


if __name__ == "__main__":

    from chunking.config import INPUT_FILE, OUTPUT_FILE

    result = run_chunking(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print(result)