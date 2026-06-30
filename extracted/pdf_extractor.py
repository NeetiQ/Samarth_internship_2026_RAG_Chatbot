import fitz
import pypdf
import os
import logging
from typing import List, Tuple

# Set up logging configuration
logger = logging.getLogger("pdf_extractor")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def extract_pdf_pages(pdf_path: str) -> Tuple[List[str], str]:
    """
    Extracts text page-by-page from a PDF file.
    Attempts extraction using PyMuPDF (fitz) first. If it fails, falls back to PyPDF.
    
    Args:
        pdf_path: Path to the PDF file.
        
    Returns:
        Tuple[List[str], str]: A tuple containing:
            - List of page texts (one string per page).
            - Name of the extractor used ('pymupdf' or 'pypdf').
            
    Raises:
        Exception: If extraction fails with both extractors or file is corrupted.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
        
    errors = []
    
    # 1. Try PyMuPDF (fitz)
    try:
        page_texts = []
        doc = fitz.open(pdf_path)
        for page in doc:
            page_texts.append(page.get_text())
        doc.close()
        
        # Simple sanity check: if doc opened but has 0 pages, or all pages are empty,
        # it might be corrupted or scanned (though prompt says digital, no OCR needed).
        # We'll treat successful opening with pages as a success.
        if len(page_texts) > 0:
            return page_texts, "pymupdf"
        else:
            raise ValueError("No pages extracted using PyMuPDF.")
            
    except Exception as e:
        err_msg = f"PyMuPDF extraction failed for {pdf_path}: {str(e)}"
        logger.warning(err_msg)
        errors.append(err_msg)
        
    # 2. Try PyPDF fallback
    try:
        page_texts = []
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            page_texts.append(text if text else "")
            
        if len(page_texts) > 0:
            logger.info(f"Successfully fell back to PyPDF for: {pdf_path}")
            return page_texts, "pypdf"
        else:
            raise ValueError("No pages extracted using PyPDF.")
            
    except Exception as e:
        err_msg = f"PyPDF extraction failed for {pdf_path}: {str(e)}"
        logger.error(err_msg)
        errors.append(err_msg)
        
    # If both failed, raise an overall exception
    raise Exception(f"All extraction methods failed for {pdf_path}. Errors: {'; '.join(errors)}")
