def build_context(chunks):

    context = ""

    for chunk in chunks:

        page_content = chunk.get("page_content", "")

        metadata = chunk.get("metadata", {})

        document_name = metadata.get(
            "document_name",
            "Unknown Document"
        )

        title = metadata.get(
            "title",
            "Unknown Title"
        )

        page = metadata.get(
            "page",
            "Unknown Page"
        )

        section = metadata.get(
            "section",
            "Unknown Section"
        )

        source = metadata.get(
            "source",
            "Unknown Source"
        )

        context += (
            f"Document: {document_name}\n"
            f"Title: {title}\n"
            f"Section: {section}\n"
            f"Page: {page}\n"
            f"Source: {source}\n\n"
            f"{page_content}\n\n"
        )

    return context.strip()