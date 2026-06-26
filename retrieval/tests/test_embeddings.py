"""
Test for loading Team A's JSONL dataset.
"""

from retrieval.pipelines.json_loader import JSONLoader

# TODO: Update this path according to your project structure
FILE_PATH = "path/to/chunked_documents.jsonl"


def main():
    documents = JSONLoader.load(FILE_PATH)

    print("=" * 60)
    print(f"Total Chunks : {len(documents)}")
    print("=" * 60)

    first_doc = documents[0]

    print("\nFirst Chunk:\n")
    print(first_doc["page_content"])

    print("\nMetadata:\n")
    for key, value in first_doc["metadata"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()