from rag_chat.workflows.retrieval_connector import retrieve_context
from rag_chat.workflows.context_builder import build_context

from rag_chat.prompts.prompt_builder import build_prompt

from rag_chat.llm.gemini_client import generate_response

from rag_chat.citations.citation_formatter import format_citations


def process_query(question, history=None):

    retrieved_data = retrieve_context(question)

    chunks = retrieved_data.get("results", [])

    if not chunks:
        return {
            "answer": "No relevant information found.",
            "citations": []
        }

    context = build_context(chunks)

    prompt = build_prompt(
        question=question,
        context=context,
        history=history
    )

    answer = generate_response(prompt)

    citations = format_citations(chunks)

    return {
        "answer": answer,
        "citations": citations
    }