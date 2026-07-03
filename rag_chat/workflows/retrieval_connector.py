import requests

from rag_chat.config import RETRIEVAL_API_URL


def retrieve_context(question, top_k=5):

    payload = {
        "query": question,
        "top_k": top_k
    }

    try:
        response = requests.post(
            RETRIEVAL_API_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Retrieval Service Error: {e}")
