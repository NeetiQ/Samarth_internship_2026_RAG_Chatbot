import os
import sys
import time
import json
import pickle
import argparse
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from typing import Dict, Any, List, Tuple

# Import custom ingestion pipeline modules
from metadata_loader import load_metadata
from pdf_extractor import extract_pdf_pages
from text_cleaner import clean_document
from document_builder import build_document

def worker_process_pdf(args: Tuple[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Worker function executed in child processes. Extracts, cleans, 
    and constructs a LangChain Document for a single judgment.
    
    Args:
        args: A tuple containing:
            - row: Dictionary of metadata for the judgment.
            - pdf_dir: Path to the directory of PDFs.
            
    Returns:
        Dict[str, Any]: Execution results containing status, counts, processing times, and document.
    """
    row, pdf_dir = args
    case_id = row.get("case_id", "")
    path_val = row.get("path", "")
    title = row.get("title", "")
    
    # 1. Locate the PDF file with fallback path naming conventions
    possible_paths = [
        os.path.join(pdf_dir, f"{path_val}_EN.pdf"),
        os.path.join(pdf_dir, f"{path_val}.pdf"),
        os.path.join(pdf_dir, path_val)
    ]
    
    pdf_path = None
    for p in possible_paths:
        if os.path.exists(p):
            pdf_path = p
            break
            
    if not pdf_path:
        return {
            "case_id": case_id,
            "path": path_val,
            "title": title,
            "status": "failed",
            "extractor": "none",
            "error_message": f"PDF file not found in any standard formats under {pdf_dir}",
            "num_pages": 0,
            "char_count": 0,
            "doc_dict": None,
            "processing_time": 0.0
        }
        
    start_time = time.time()
    try:
        # 2. Extract page-by-page text
        page_texts, extractor_name = extract_pdf_pages(pdf_path)
        
        # 3. Clean the text using the metadata row
        cleaned_text = clean_document(page_texts, row)
        
        # 4. Build standard LangChain Document object
        doc = build_document(cleaned_text, row)
        doc_dict = {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        
        elapsed = time.time() - start_time
        return {
            "case_id": case_id,
            "path": path_val,
            "title": title,
            "status": "success",
            "extractor": extractor_name,
            "error_message": None,
            "num_pages": len(page_texts),
            "char_count": len(cleaned_text),
            "doc_dict": doc_dict,
            "processing_time": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "case_id": case_id,
            "path": path_val,
            "title": title,
            "status": "failed",
            "extractor": "none",
            "error_message": str(e),
            "num_pages": 0,
            "char_count": 0,
            "doc_dict": None,
            "processing_time": elapsed
        }

def save_reports(results_list: List[Dict[str, Any]], report_path: str, failed_path: str, resume_mode: bool):
    """
    Saves or appends process metrics and failure reports.
    """
    new_report_rows = []
    new_failed_rows = []
    
    for r in results_list:
        new_report_rows.append({
            "case_id": r["case_id"],
            "path": r["path"],
            "title": r["title"],
            "status": r["status"],
            "extractor": r["extractor"],
            "error_message": r["error_message"] or "",
            "num_pages": r["num_pages"],
            "char_count": r["char_count"],
            "processing_time_sec": round(r["processing_time"], 3)
        })
        if r["status"] == "failed":
            new_failed_rows.append({
                "case_id": r["case_id"],
                "path": r["path"],
                "title": r["title"],
                "error_message": r["error_message"] or ""
            })
            
    df_new_report = pd.DataFrame(new_report_rows)
    df_new_failed = pd.DataFrame(new_failed_rows)
    
    # Save/append processing report
    write_header = not (resume_mode and os.path.exists(report_path))
    mode = "a" if (resume_mode and os.path.exists(report_path)) else "w"
    if not df_new_report.empty:
        df_new_report.to_csv(report_path, mode=mode, header=write_header, index=False)
        
    # Save/append failed report
    write_failed_header = not (resume_mode and os.path.exists(failed_path))
    failed_mode = "a" if (resume_mode and os.path.exists(failed_path)) else "w"
    if not df_new_failed.empty:
        df_new_failed.to_csv(failed_path, mode=failed_mode, header=write_failed_header, index=False)
    elif not os.path.exists(failed_path):
        pd.DataFrame(columns=["case_id", "path", "title", "error_message"]).to_csv(failed_path, index=False)

def sync_pkl_from_jsonl(jsonl_path: str, pkl_path: str):
    """
    Reconstructs the full Python List[Document] from documents.jsonl
    and dumps it as documents.pkl. Ensures pkl contains all processed docs.
    """
    try:
        from langchain.schema import Document
    except ImportError:
        from langchain_core.documents import Document
    
    documents = []
    if os.path.exists(jsonl_path):
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    doc = Document(
                        page_content=data["page_content"],
                        metadata=data["metadata"]
                    )
                    documents.append(doc)
                    
    with open(pkl_path, "wb") as f:
        pickle.dump(documents, f)
    print(f"Successfully synchronized {len(documents)} LangChain Document objects to {pkl_path}")

def main():
    parser = argparse.ArgumentParser(description="Legal RAG Ingestion Pipeline")
    parser.add_argument("--metadata_path", type=str, default=r"C:\Users\krish\Downloads\metadata.parquet",
                        help="Path to metadata.parquet")
    parser.add_argument("--pdf_dir", type=str, default=r"C:\Users\krish\Downloads\english",
                        help="Directory containing judgment PDFs")
    parser.add_argument("--output_dir", type=str, default=".",
                        help="Output directory to save reports and documents")
    parser.add_argument("--num_processes", type=int, default=os.cpu_count(),
                        help="Number of parallel processes")
    parser.add_argument("--no_resume", action="store_true",
                        help="Disable resuming and overwrite existing outputs")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    jsonl_path = os.path.join(args.output_dir, "documents.jsonl")
    pkl_path = os.path.join(args.output_dir, "documents.pkl")
    report_path = os.path.join(args.output_dir, "processing_report.csv")
    failed_path = os.path.join(args.output_dir, "failed_files.csv")
    
    # Check for resuming status
    processed_case_ids = set()
    resume_mode = not args.no_resume
    
    if resume_mode and os.path.exists(report_path):
        try:
            existing_report = pd.read_csv(report_path)
            if "case_id" in existing_report.columns:
                processed_case_ids = set(existing_report["case_id"].astype(str).tolist())
                print(f"Found existing processing report. Skipping {len(processed_case_ids)} already processed cases.")
        except Exception as e:
            print(f"Could not load existing report for resuming, starting fresh: {e}")
            resume_mode = False
            
    # Load metadata
    print("Loading metadata...")
    df_meta = load_metadata(args.metadata_path)
    print(f"Total rows in metadata: {len(df_meta)}")
    
    # Filter rows to process
    if resume_mode and processed_case_ids:
        df_to_process = df_meta[~df_meta["case_id"].astype(str).isin(processed_case_ids)]
    else:
        df_to_process = df_meta
        
    print(f"Pending files to process: {len(df_to_process)}")
    
    if len(df_to_process) == 0:
        print("No new files to process.")
        if not os.path.exists(failed_path):
            pd.DataFrame(columns=["case_id", "path", "title", "error_message"]).to_csv(failed_path, index=False)
        sync_pkl_from_jsonl(jsonl_path, pkl_path)
        return
        
    # Open jsonl file in append or write mode
    open_mode = "a" if (resume_mode and os.path.exists(jsonl_path)) else "w"
    
    # Prepare task arguments
    tasks = [(row.to_dict(), args.pdf_dir) for _, row in df_to_process.iterrows()]
    
    results_list = []
    
    print(f"Starting multiprocessing pool with {args.num_processes} workers...")
    
    with open(jsonl_path, open_mode, encoding="utf-8") as f_jsonl:
        with Pool(processes=args.num_processes) as pool:
            # We iterate over results as they complete to show live progress and write to jsonl incrementally
            for result in tqdm(pool.imap_unordered(worker_process_pdf, tasks), total=len(tasks), desc="Processing PDFs"):
                results_list.append(result)
                
                # Write successfully processed documents directly to file
                if result["status"] == "success" and result["doc_dict"]:
                    f_jsonl.write(json.dumps(result["doc_dict"], ensure_ascii=False) + "\n")
                    f_jsonl.flush()
                    
    # Generate reports and dump pickle file
    print("Saving processing reports...")
    save_reports(results_list, report_path, failed_path, resume_mode)
    
    print("Synchronizing documents.pkl with documents.jsonl...")
    sync_pkl_from_jsonl(jsonl_path, pkl_path)
    
    print("Pipeline run finished successfully!")

if __name__ == "__main__":
    main()
