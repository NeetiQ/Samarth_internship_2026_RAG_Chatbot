def format_citations(metadata_list):

    citations = []

    for metadata in metadata_list:

        source = metadata.get("source", "Unknown Source")
        page = metadata.get("page", "Unknown Page")

        citation = f"Source: {source} | Page: {page}"

        if citation not in citations:
            citations.append(citation)

    return citations