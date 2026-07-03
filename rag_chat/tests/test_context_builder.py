from rag_chat.workflows.context_builder import build_context


def test_build_context():

    chunks = [
        "Tenant must provide 30 days notice.",
        "Rent should be paid before the 5th of every month."
    ]

    context = build_context(chunks)

    assert "[Source 1]" in context
    assert "[Source 2]" in context
    assert "Tenant must provide 30 days notice." in context
    assert "Rent should be paid before the 5th of every month." in context


def test_build_context_empty():

    context = build_context([])

    assert context == ""