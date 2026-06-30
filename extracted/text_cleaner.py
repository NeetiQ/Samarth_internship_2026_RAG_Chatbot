import re
from typing import List, Dict

def normalize_string(s: str) -> str:
    """
    Normalizes string by converting to lowercase and stripping all non-alphanumeric characters.
    Used for safe header matches of title strings.
    """
    return re.sub(r'[^a-z0-9]', '', s.lower())

def clean_page(page_text: str, page_idx: int, metadata: Dict[str, str]) -> str:
    """
    Cleans raw text from a single page using metadata context.
    
    Args:
        page_text: Raw string extracted from a PDF page.
        page_idx: 0-indexed page number of the page.
        metadata: Metadata dictionary containing details like 'title'.
        
    Returns:
        str: Cleaned page text.
    """
    lines = page_text.split("\n")
    cleaned_lines = []
    
    title = metadata.get("title", "")
    norm_title = normalize_string(title)
    
    total_lines = len(lines)
    
    for line_idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not line:
            cleaned_lines.append("")
            continue
            
        # 1. Check for standalone page numbers (only in top 4 or bottom 4 lines)
        is_near_boundary = (line_idx < 4) or (line_idx > total_lines - 5)
        if is_near_boundary:
            # Matches digits with optional backspaces or whitespace
            if re.match(r'^[\x08]*\d+[\x08]*$', line):
                continue
                
        # 2. Check for repeated headers/footers (only on page 2 and later, i.e., index >= 1)
        if page_idx >= 1:
            line_lower = line.lower()
            
            # Match standard static headers
            if "digital supreme court reports" in line_lower:
                continue
                
            # Citation header: e.g., "[2025] 1 S.C.R." or "[2025] 1 S.C.R. \x08"
            # Note the $ anchor at the end - this preserves full citations like "[2025] 1 S.C.R. 81"
            if re.match(r'^\[\d{4}\]\s+\d+\s+S\.C\.R\.[\s\x08]*$', line):
                continue
                
            # Case title check (top lines of the page)
            if line_idx < 4 and len(line) >= 10:
                norm_line = normalize_string(line)
                if norm_line and norm_line in norm_title:
                    continue
                    
        # 3. Check for download notices / signatures (on all pages)
        line_lower = line.lower()
        notices = [
            "digitally signed by",
            "signature not verified",
            "downloaded from",
            "certified copy",
            "authenticated copy",
            "copy from"
        ]
        if any(msg in line_lower for msg in notices):
            continue
            
        # Clean line contents: remove backspaces and clean spacing
        line_cleaned = raw_line.replace("\x08", "")
        line_cleaned = re.sub(r'\s+', ' ', line_cleaned).strip()
        cleaned_lines.append(line_cleaned)
        
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text

def clean_document(page_texts: List[str], metadata: Dict[str, str]) -> str:
    """
    Cleans raw extracted page texts of a document using metadata.
    
    Args:
        page_texts: List of strings (one per page).
        metadata: Metadata dictionary containing details like 'title'.
        
    Returns:
        str: Fully cleaned judgment text.
    """
    cleaned_pages = []
    for idx, page_text in enumerate(page_texts):
        cleaned_page = clean_page(page_text, idx, metadata)
        cleaned_pages.append(cleaned_page)
        
    doc_text = "\n\n".join(cleaned_pages)
    # Reduce multiple blank lines (3 or more newlines) to exactly 2 newlines (one empty line)
    doc_text = re.sub(r'\n{3,}', '\n\n', doc_text)
    return doc_text.strip()
