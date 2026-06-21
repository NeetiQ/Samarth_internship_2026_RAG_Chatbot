from .models import ChatResponse


class ChatWorkflow:

    def __init__(self, retrieval_service, prompt_service,
                 llm_service, citation_service):
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service
        self.llm_service = llm_service
        self.citation_service = citation_service

    def process_query(self, query: str):

        # Step 1: Retrieve context
        retrieved_data = self.retrieval_service.retrieve(query)

        chunks = retrieved_data.get("chunks", [])

        # Step 2: Build prompt
        prompt = self.prompt_service.build_prompt(
            query=query,
            chunks=chunks
        )

        # Step 3: Generate answer
        answer = self.llm_service.generate(prompt)

        # Step 4: Generate citations
        citations = self.citation_service.generate(
            retrieved_data
        )

        return ChatResponse(
            answer=answer,
            citations=citations
        )