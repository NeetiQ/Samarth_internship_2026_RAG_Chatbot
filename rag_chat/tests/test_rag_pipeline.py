from rag_chat.workflows.rag_pipeline import RAGPipeline


class MockRetrievalConnector:
    def retrieve(self, query):
        return {
            "chunks": ["Sample legal chunk"],
            "metadata": [
                {
                    "source": "test.pdf",
                    "page": 1
                }
            ]
        }


class MockLLMClient:
    def generate(self, prompt):
        return "This is a generated answer"


def test_process_query():

    pipeline = RAGPipeline(
        retrieval_connector=MockRetrievalConnector(),
        llm_client=MockLLMClient()
    )

    response = pipeline.process_query(
        "What is the notice period?"
    )

    assert response["answer"] == "This is a generated answer"
    assert len(response["citations"]) == 1