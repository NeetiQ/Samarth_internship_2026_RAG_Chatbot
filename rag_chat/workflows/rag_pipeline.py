class RAGPipeline:

    def __init__(
        self,
        retrieval_service,
        prompt_service,
        llm_service,
        citation_service
    ):
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service
        self.llm_service = llm_service
        self.citation_service = citation_service

    def process_query(self, query):

        retrieved_data = self.retrieval_service.retrieve(query)

        chunks = retrieved_data.get("chunks", [])

        prompt = self.prompt_service.build_prompt(
            query=query,
            chunks=chunks
        )

        answer = self.llm_service.generate(prompt)

        citations = self.citation_service.generate(
            retrieved_data
        )

        return {
            "answer": answer,
            "citations": citations
        }