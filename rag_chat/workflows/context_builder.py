class ContextBuilder:

    def build_context(self, chunks):

        context = ""

        for idx, chunk in enumerate(chunks, start=1):
            context += f"\n[Source {idx}]\n{chunk}\n"

        return context