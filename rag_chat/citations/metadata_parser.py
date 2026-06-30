def parse_metadata(chunk):

    metadata = chunk.get("metadata", {})

    return {
        "document_name": metadata.get(
            "document_name",
            "Unknown Document"
        ),

        "title": metadata.get(
            "title",
            "Unknown Title"
        ),

        "page": metadata.get(
            "page",
            "Unknown Page"
        ),

        "section": metadata.get(
            "section",
            "Unknown Section"
        ),

        "source": metadata.get(
            "source",
            "Unknown Source"
        )
    }