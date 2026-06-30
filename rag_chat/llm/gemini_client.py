from google import genai

from rag_chat.config import GEMINI_API_KEY
from rag_chat.llm.model_config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    TOP_P,
    TOP_K
)


def configure_client():

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY not found.")

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt):

    client = configure_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "top_p": TOP_P,
            "top_k": TOP_K
        }
    )

    text = getattr(response, "text", "")
    return clean_response(text)


def clean_response(response):

    return response.strip()
