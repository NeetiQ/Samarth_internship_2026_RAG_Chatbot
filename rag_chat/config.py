import os


def get_gemini_key():
    return os.getenv("GEMINI_API_KEY")


RETRIEVAL_API_URL = os.getenv("RETRIEVAL_API_URL")

CHAT_HISTORY_ENABLED = (
    os.getenv("CHAT_HISTORY_ENABLED", "true").lower() == "true"
)

MAX_CHAT_HISTORY_MESSAGES = int(
    os.getenv("MAX_CHAT_HISTORY_MESSAGES", 10)
)

ENABLE_CITATIONS = (
    os.getenv("ENABLE_CITATIONS", "true").lower() == "true"
)

CITATION_STYLE = os.getenv("CITATION_STYLE", "apa")