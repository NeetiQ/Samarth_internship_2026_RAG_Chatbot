def build_context(chunks):

    context = ""

    for idx, chunk in enumerate(chunks, start=1):
        context += f"[Source {idx}]\n{chunk}\n\n"

    return context.strip()