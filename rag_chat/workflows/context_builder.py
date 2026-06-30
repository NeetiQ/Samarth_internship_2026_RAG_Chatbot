def build_context(chunks):

    context = ""

    for chunk in chunks:

        source = chunk.get("source", "Unknown Source")
        page = chunk.get("page", "Unknown Page")
        text = chunk.get("text", "")

        context += f"Source: {source}\n"
        context += f"Page: {page}\n\n"
        context += f"{text}\n\n"

    return context.strip()