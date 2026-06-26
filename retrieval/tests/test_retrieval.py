from retrieval.search.retriever import Retriever


def main():

    retriever = Retriever()

    query = "What is anticipatory bail?"

    results = retriever.retrieve(query)

    print(f"\nRetrieved {len(results)} chunks\n")

    for i, result in enumerate(results, start=1):

        print("=" * 80)
        print(f"Result {i}")
        print(f"Score: {result['score']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Title: {result['metadata'].get('title')}")
        print(f"Citation: {result['metadata'].get('citation')}")
        print()
        print(result["page_content"][:500])
        print()


if __name__ == "__main__":
    main()