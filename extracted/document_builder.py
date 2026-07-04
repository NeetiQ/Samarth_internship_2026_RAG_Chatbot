try:
    from langchain.schema import Document
except ImportError:
    from langchain_core.documents import Document
from typing import Dict, Any

def build_document(cleaned_judgment_text: str, row: Dict[str, Any]) -> Document:
    """
    Constructs a LangChain Document object from cleaned text and metadata row.
    
    Args:
        cleaned_judgment_text: The cleaned judgment text.
        row: A dictionary containing metadata fields.
        
    Returns:
        Document: A LangChain Document object matching the required schema.
    """
    return Document(
        page_content=cleaned_judgment_text,
        metadata={
            "title": row.get("title", ""),
            "case_id": row.get("case_id", ""),
            "court": row.get("court", ""),
            "year": row.get("year", ""),
            "decision_date": row.get("decision_date", ""),
            "citation": row.get("citation", ""),
            "judge": row.get("judge", ""),
            "path": row.get("path", "")
        }
    )
