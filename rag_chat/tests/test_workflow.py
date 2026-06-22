from rag_chat.workflows.chat_workflow import ChatWorkflow


class MockRetrievalService:
    def retrieve(self, query):
        return {
            "chunks": ["Sample legal chunk"],
            "metadata": []
        }

class MockPromptService:
    def build_prompt(self, query, chunks):
        return f"Question: {query}\nContext: {chunks}"


class MockLLMService:
    def generate(self, prompt):
        return "This is a generated answer"


class MockCitationService:
    def generate(self, retrieved_data):
        return [
            {
                "source": "test.pdf",
                "page": 1
            }
        ]


def test_process_query():

    workflow = ChatWorkflow(
        retrieval_service=MockRetrievalService(),
        prompt_service=MockPromptService(),
        llm_service=MockLLMService(),
        citation_service=MockCitationService()
    )

    response = workflow.process_query(
        "What is the notice period?"
    )

    assert response.answer == "This is a generated answer"
    assert len(response.citations) == 1
    