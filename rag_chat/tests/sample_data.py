MOCK_QUESTION = "What is anticipatory bail?"


MOCK_PROMPT = """
You are a legal assistant.

Question:
What is anticipatory bail?

Answer in 2-3 sentences.
"""


MOCK_HISTORY = [
    {
        "role": "user",
        "content": "What is bail?"
    },
    {
        "role": "assistant",
        "content": (
            "Bail is the temporary release of an accused person "
            "while awaiting trial."
        )
    }
]


MOCK_CHUNKS = [
    {
        "chunk_id": "chunk_001",
        "page_content": (
            "Section 438 of the Code of Criminal Procedure "
            "provides provisions relating to anticipatory bail."
        ),
        "metadata": {
            "document_name": "CrPC.pdf",
            "title": "Code of Criminal Procedure",
            "page": 45,
            "section": "Section 438",
            "source": "Supreme Court Database"
        },
        "score": 0.94
    },
    {
        "chunk_id": "chunk_002",
        "page_content": (
            "Anticipatory bail protects a person from arrest "
            "before the actual arrest takes place."
        ),
        "metadata": {
            "document_name": "CrPC.pdf",
            "title": "Code of Criminal Procedure",
            "page": 46,
            "section": "Section 438",
            "source": "Supreme Court Database"
        },
        "score": 0.92
    }
]