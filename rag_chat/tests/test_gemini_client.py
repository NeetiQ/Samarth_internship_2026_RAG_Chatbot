from rag_chat.llm.gemini_client import (
    configure_client,
    generate_response
)

from rag_chat.config import GEMINI_API_KEY

from rag_chat.tests.sample_data import MOCK_PROMPT


def test_gemini_client():

    assert GEMINI_API_KEY is not None
    assert GEMINI_API_KEY.strip() != ""

    client = configure_client()

    assert client is not None

    response = generate_response(MOCK_PROMPT)

    assert response is not None
    assert isinstance(response, str)
    assert len(response.strip()) > 0

    print("\nGemini Response:\n")
    print(response)

    print("\nGemini Client Test Passed Successfully!")


if __name__ == "__main__":
    test_gemini_client()