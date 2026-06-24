"""
Test semantic search.
"""

from retrieval.search.retriever import Retriever


def main():

    retriever = Retriever()

    query = "What is anticipatory bail?"

    results = retriever.retrieve(query)

    print(f"\nRetrieved {len(results)} results.\n")

    for index, result in enumerate(results, start=1):

        print("=" * 80)
        print(f"Result {index}")
        print(f"Score      : {result['score']:.4f}")
        print(f"Chunk ID   : {result['chunk_id']}")
        print(f"Metadata   : {result['metadata']}")
        print(f"Content    :\n{result['page_content'][:300]}")
        print()


if __name__ == "__main__":
    main()