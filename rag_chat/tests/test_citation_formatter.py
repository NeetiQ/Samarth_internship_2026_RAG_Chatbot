from rag_chat.citations.citation_formatter import format_citations


def test_format_citations():

    metadata = [
        {
            "source": "lease.pdf",
            "page": 5
        },
        {
            "source": "agreement.pdf",
            "page": 10
        }
    ]

    citations = format_citations(metadata)

    assert len(citations) == 2
    assert "Source: lease.pdf | Page: 5" in citations
    assert "Source: agreement.pdf | Page: 10" in citations


def test_duplicate_citations():

    metadata = [
        {
            "source": "lease.pdf",
            "page": 5
        },
        {
            "source": "lease.pdf",
            "page": 5
        }
    ]

    citations = format_citations(metadata)

    assert len(citations) == 1