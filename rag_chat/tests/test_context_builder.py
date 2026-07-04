from rag_chat.workflows.context_builder import build_context

from rag_chat.tests.sample_data import MOCK_CHUNKS


def test_context_builder():

    context = build_context(MOCK_CHUNKS)

    assert context is not None
    assert isinstance(context, str)
    assert len(context.strip()) > 0

    assert "CrPC.pdf" in context
    assert "Code of Criminal Procedure" in context
    assert "Section 438" in context
    assert "Supreme Court Database" in context
    assert "Anticipatory bail" in context

    print("\nGenerated Context:\n")
    print(context)

    print("\nContext Builder Test Passed Successfully!")


if __name__ == "__main__":
    test_context_builder()