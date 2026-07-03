from rag_chat.prompts.prompt_builder import build_prompt


def test_prompt_builder():

    question = "What is anticipatory bail?"

    context = """
Document: CrPC.pdf
Title: Code of Criminal Procedure
Section: Section 438
Page: 45
Source: Supreme Court Database

Section 438 of the Code of Criminal Procedure provides provisions relating to anticipatory bail.
"""

    history = [
        {
            "role": "user",
            "content": "What is bail?"
        },
        {
            "role": "assistant",
            "content": "Bail is the temporary release of an accused person while awaiting trial."
        }
    ]

    prompt = build_prompt(
        question=question,
        context=context,
        history=history
    )

    assert question in prompt
    assert "Section 438" in prompt
    assert "Code of Criminal Procedure" in prompt
    assert "What is bail?" in prompt
    assert "Bail is the temporary release" in prompt

    print("\nGenerated Prompt:\n")
    print(prompt)

    print("\nPrompt Builder Test Passed Successfully!")


if __name__ == "__main__":
    test_prompt_builder()