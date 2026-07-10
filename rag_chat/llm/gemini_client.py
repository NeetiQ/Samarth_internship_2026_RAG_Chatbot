import os

from google import genai

from rag_chat.llm.model_config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    TOP_P,
    TOP_K,
)


def get_available_keys():
    """
    Collect all configured Gemini API keys from the environment.

    Supports:
        GEMINI_API_KEY
        GEMINI_API_KEY_2
        GEMINI_API_KEY_3
        ...
    """

    keys = []

    primary = os.getenv("GEMINI_API_KEY")
    if primary:
        keys.append(primary)

    i = 2
    while True:
        key = os.getenv(f"GEMINI_API_KEY_{i}")

        if not key:
            break

        keys.append(key)
        i += 1

    return keys


def generate_response(prompt):
    """
    Generate a response using Gemini.

    Automatically falls back through all configured API keys
    if a key is exhausted, rate limited, or temporarily unavailable.
    """

    keys = get_available_keys()

    if not keys:
        raise ValueError("No Gemini API keys found.")

    last_error = None

    for index, key in enumerate(keys, start=1):

        print(f"\nTrying Gemini API Key {index}", flush=True)

        try:
            client = genai.Client(api_key=key)

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": TEMPERATURE,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                    "top_p": TOP_P,
                    "top_k": TOP_K,
                },
            )

            text = getattr(response, "text", "")

            print(f"Gemini API Key {index} succeeded.", flush=True)

            return clean_response(text)

        except Exception as error:

            print(
                f"Gemini API Key {index} failed:\n{error}",
                flush=True,
            )

            last_error = error

            continue

    raise RuntimeError(
        f"All Gemini API keys failed.\nLast error:\n{last_error}"
    )


def clean_response(response):

    return response.strip() if response else ""