from rag_chat.citations.citation_formatter import format_citations

from tests.sample_data import MOCK_CHUNKS


def test_citation_formatter():

    citations = format_citations(MOCK_CHUNKS)

    assert citations is not None
    assert isinstance(citations, list)
    assert len(citations) == 2

    assert "Code of Criminal Procedure" in citations[0]
    assert "CrPC.pdf" in citations[0]
    assert "Section 438" in citations[0]
    assert "Supreme Court Database" in citations[0]

    print("\nGenerated Citations:\n")

    for citation in citations:
        print(citation)

    print("\nCitation Formatter Test Passed Successfully!")


if __name__ == "__main__":
    test_citation_formatter()