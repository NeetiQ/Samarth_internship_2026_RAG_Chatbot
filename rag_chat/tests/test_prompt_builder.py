from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.workflows.context_builder import build_context

from rag_chat.tests.sample_data import (
    MOCK_QUESTION,
    MOCK_HISTORY,
    MOCK_CHUNKS
)


def test_prompt_builder():

    context = build_context(MOCK_CHUNKS)

    prompt = build_prompt(
        question=MOCK_QUESTION,
        context=context,
        history=MOCK_HISTORY
    )

    assert MOCK_QUESTION in prompt
    assert "Section 438" in prompt
    assert "Code of Criminal Procedure" in prompt
    assert "What is bail?" in prompt
    assert "Bail is the temporary release" in prompt

    print("\nGenerated Prompt:\n")
    print(prompt)

    print("\nPrompt Builder Test Passed Successfully!")


if __name__ == "__main__":
    test_prompt_builder()