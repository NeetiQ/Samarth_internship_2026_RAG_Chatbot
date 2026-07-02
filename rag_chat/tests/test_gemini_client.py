from unittest.mock import patch

from rag_chat.llm.gemini_client import clean_response


def test_clean_response():

    response = "  Hello World  "

    assert clean_response(response) == "Hello World"


@patch("rag_chat.llm.gemini_client.configure_client")
def test_generate_response(mock_client):

    mock_response = type(
        "MockResponse",
        (),
        {"text": "Generated Answer"}
    )()

    mock_client.return_value.models.generate_content.return_value = mock_response

    from rag_chat.llm.gemini_client import generate_response

    result = generate_response("Test Prompt")

    assert result == "Generated Answer"