from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import sys
import os

# Add root of the project to path for Team A's scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from extracted.pdf_extractor import extract_pdf_pages
from extracted.text_cleaner import clean_document

from app.repositories import job_repo, document_repo, chunk_repo
from app.models.all_models import ProcessingStage
from app.database.session import AsyncSessionLocal
import asyncio

class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @classmethod
    async def process_document_background(cls, document_id: int):
        """Runs the real-time ingestion pipeline with its own DB session."""
        async with AsyncSessionLocal() as db:
            service = cls(db)
            await service._process_document(document_id)

    async def _process_document(self, document_id: int):
        """Runs the real-time ingestion pipeline asynchronously."""
        job = await job_repo.get_by_document_id(self.db, document_id)
        if not job:
            return
            
        try:
            # Get document details
            doc = await document_repo.get(self.db, id=document_id)
            if not doc:
                raise Exception("Document not found")
                
            pdf_path = doc.file_path

            # 2. Extract & Clean
            await job_repo.update(self.db, db_obj=job, obj_in={"stage": ProcessingStage.EXTRACTION, "status": "in_progress"})
            
            # Run blocking Team A code in an executor
            loop = asyncio.get_event_loop()
            page_texts, _ = await loop.run_in_executor(None, extract_pdf_pages, pdf_path)
            
            # Simulated metadata for cleaner
            dummy_meta = {"case_id": doc.id, "title": doc.title}
            cleaned_text = await loop.run_in_executor(None, clean_document, page_texts, dummy_meta)
            
            # 3. Chunking
            await job_repo.update(self.db, db_obj=job, obj_in={"stage": ProcessingStage.CHUNKING})
            
            from chunking.chunker import DocumentChunker
            from langchain_core.documents import Document
            
            def do_chunk(text, doc_id):
                chunker = DocumentChunker()
                doc = Document(page_content=text, metadata={"case_id": str(doc_id)})
                chunked = chunker.chunk_documents([doc])
                return [c.page_content for c in chunked]
                
            chunks = await loop.run_in_executor(None, do_chunk, cleaned_text, document_id)
            
            # 4. Save Chunks & Generate Embeddings
            from retrieval.embeddings.embedder import Embedder
            embedder = await loop.run_in_executor(None, Embedder)
            
            # Generate embeddings in batch
            embeddings = await loop.run_in_executor(None, embedder.encode_batch, chunks)
            
            for idx, c in enumerate(chunks):
                chunk_id_str = f"doc_{document_id}_chunk_{idx}"
                await chunk_repo.create(self.db, obj_in={
                    "document_id": document_id,
                    "chunk_id": chunk_id_str,
                    "page_content": c,
                    "embedding": embeddings[idx]
                })

            # 5. Completed
            await job_repo.update(self.db, db_obj=job, obj_in={
                "stage": ProcessingStage.COMPLETED, 
                "status": "completed",
                "completed_at": datetime.utcnow()
            })
            
        except Exception as e:
            await job_repo.update(self.db, db_obj=job, obj_in={
                "status": "failed", 
                "error_message": str(e),
                "completed_at": datetime.utcnow()
            })
