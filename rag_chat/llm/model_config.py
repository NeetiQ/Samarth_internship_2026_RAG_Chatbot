import os

MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.5-flash")

TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.3))

MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", 1024))

TOP_P = float(os.getenv("TOP_P", 0.95))

TOP_K = int(os.getenv("TOP_K", 40))