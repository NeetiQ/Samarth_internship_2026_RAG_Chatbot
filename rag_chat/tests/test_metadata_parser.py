from rag_chat.citations.metadata_parser import parse_metadata


def test_metadata_parser():

    chunk = {
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
    }

    metadata = parse_metadata(chunk)

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