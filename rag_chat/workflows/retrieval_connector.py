from retrieval.search.retriever import Retriever

retriever = Retriever()


def retrieve_context(question, top_k=5):

    results = retriever.retrieve(
        query=question,
        top_k=top_k,
    )

    return {
        "query": question,
        "count": len(results),
        "results": results,
    }