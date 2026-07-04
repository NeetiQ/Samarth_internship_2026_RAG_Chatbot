from rag_chat.workflows.context_builder import build_context
from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.llm.gemini_client import generate_response
from rag_chat.citations.citation_formatter import format_citations

from tests.sample_data import (
    QUESTION,
    HISTORY,
    CHUNKS
)


def test_rag_pipeline():

    context = build_context(CHUNKS)

    prompt = build_prompt(
        question=QUESTION,
        context=context,
        history=HISTORY
    )

    answer = generate_response(prompt)

    citations = format_citations(CHUNKS)

    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    assert citations is not None
    assert isinstance(citations, list)
    assert len(citations) > 0

    print("\nQuestion:\n")
    print(QUESTION)

    print("\nGenerated Answer:\n")
    print(answer)

    print("\nCitations:\n")

    for citation in citations:
        print(citation)

    print("\nRAG Pipeline Test Passed Successfully!")


if __name__ == "__main__":
    test_rag_pipeline()