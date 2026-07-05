from rag_chat.citations.metadata_parser import parse_metadata

from rag_chat.tests.sample_data import MOCK_CHUNKS


def test_metadata_parser():

    metadata = parse_metadata(MOCK_CHUNKS[0])

    assert metadata["document_name"] == "CrPC.pdf"
    assert metadata["title"] == "Code of Criminal Procedure"
    assert metadata["page"] == 45
    assert metadata["section"] == "Section 438"
    assert metadata["source"] == "Supreme Court Database"

    print("\nParsed Metadata:\n")
    print(metadata)

    print("\nMetadata Parser Test Passed Successfully!")


if __name__ == "__main__":
    test_metadata_parser()