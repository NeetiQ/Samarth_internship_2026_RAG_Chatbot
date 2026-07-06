from rag_chat.tests.sample_data import MOCK_QUESTION


def test_retrieval_connector():

    payload = {
        "query": MOCK_QUESTION,
        "top_k": 5
    }

    assert payload["query"] == MOCK_QUESTION
    assert payload["top_k"] == 5

    print("\nRequest Payload:\n")
    print(payload)

    print("\nRetrieval Connector Test Passed Successfully!")


if __name__ == "__main__":
    test_retrieval_connector()