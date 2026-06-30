from rag_chat.citations.metadata_parser import parse_metadata


def format_citations(chunks):

    citations = []

    for chunk in chunks:

        metadata = parse_metadata(chunk)

        citation = (
            f"Title: {metadata['title']} | "
            f"Document: {metadata['document_name']} | "
            f"Section: {metadata['section']} | "
            f"Page: {metadata['page']} | "
            f"Source: {metadata['source']}"
        )

        if citation not in citations:
            citations.append(citation)

    return citations