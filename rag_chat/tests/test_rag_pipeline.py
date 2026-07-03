from rag_chat.workflows.context_builder import build_context
from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.llm.gemini_client import generate_response
from rag_chat.citations.citation_formatter import format_citations


def test_rag_pipeline():

    question = "What is anticipatory bail?"

    history = []

    chunks = [
        {
            "chunk_id": "chunk_001",
            "page_content": (
                "Section 438 of the Code of Criminal Procedure "
                "provides provisions relating to anticipatory bail."
            ),
            "metadata": {
                "document_name": "CrPC.pdf",
                "title": "Code of Criminal Procedure",
                "page": 45,
                "section": "Section 438",
                "source": "Supreme Court Database"
            },
            "score": 0.94
        }
    ]

    context = build_context(chunks)

    prompt = build_prompt(
        question=question,
        context=context,
        history=history
    )

    answer = generate_response(prompt)

    citations = format_citations(chunks)

    print("\nQuestion:\n")
    print(question)

    print("\nGenerated Answer:\n")
    print(answer)

    print("\nCitations:\n")

    for citation in citations:
        print(citation)


if __name__ == "__main__":
    test_rag_pipeline()