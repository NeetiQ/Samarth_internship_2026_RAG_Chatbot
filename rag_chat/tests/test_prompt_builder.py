from rag_chat.prompts.prompt_builder import build_prompt
from rag_chat.workflows.context_builder import build_context

from tests.sample_data import (
    QUESTION,
    HISTORY,
    CHUNKS
)


def test_prompt_builder():

    context = build_context(CHUNKS)

    prompt = build_prompt(
        question=QUESTION,
        context=context,
        history=HISTORY
    )

    assert QUESTION in prompt
    assert "Section 438" in prompt
    assert "Code of Criminal Procedure" in prompt
    assert "What is bail?" in prompt
    assert "Bail is the temporary release" in prompt

    print("\nGenerated Prompt:\n")
    print(prompt)

    print("\nPrompt Builder Test Passed Successfully!")


if __name__ == "__main__":
    test_prompt_builder()