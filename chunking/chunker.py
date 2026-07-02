import json
import logging
import hashlib
from typing import List

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class DocumentChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\nIssue for Consideration",
                "\nHeadnotes",
                "\nJUDGMENT",
                "\nJudgment",
                "\nORDER",
                "\nOrder",
                "\nFacts",
                "\nFACTS",
                "\nAnalysis",
                "\nReasoning",
                "\nHeld",
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def load_documents(self, jsonl_path: str) -> List[Document]:

        documents = []

        with open(jsonl_path, "r", encoding="utf-8") as file:

            for line in file:

                if not line.strip():
                    continue

                data = json.loads(line)

                documents.append(
                    Document(
                        page_content=data["page_content"],
                        metadata=data["metadata"]
                    )
                )

        logger.info(f"Loaded {len(documents)} documents")

        return documents

    def chunk_documents(self, documents: List[Document]) -> List[Document]:

        chunked_documents = []

        seen_chunk_ids = set()

        for doc in documents:

            chunks = self.splitter.split_text(doc.page_content)

            case_id = doc.metadata.get(
                "case_id",
                "unknown"
            )

            source = doc.metadata.get(
                "path",
                ""
            )

            # Create a unique document signature
            document_signature = hashlib.sha256(
                (
                    source + doc.page_content
                ).encode("utf-8")
            ).hexdigest()

            total_chunks = len(chunks)

            for idx, chunk_text in enumerate(chunks):

                if not chunk_text.strip():
                    continue

                metadata = dict(doc.metadata)

                # Stable unique document ID
                metadata["doc_id"] = document_signature

                # Stable unique chunk ID
                chunk_id = hashlib.sha256(
                    (
                        document_signature +
                        "_" +
                        str(idx)
                    ).encode("utf-8")
                ).hexdigest()

                # Safety check
                if chunk_id in seen_chunk_ids:
                    raise ValueError(
                        f"Duplicate chunk_id generated: {chunk_id}"
                    )

                seen_chunk_ids.add(chunk_id)

                metadata["chunk_id"] = chunk_id
                metadata["source"] = source
                metadata["chunk_index"] = idx
                metadata["total_chunks"] = total_chunks
                metadata["chunk_length"] = len(chunk_text)

                chunked_documents.append(
                    Document(
                        page_content=chunk_text,
                        metadata=metadata
                    )
                )

        logger.info(
            f"Generated {len(chunked_documents)} chunks"
        )

        logger.info(
            f"Verified {len(seen_chunk_ids)} unique chunk IDs"
        )

        return chunked_documents

    def save_chunks(
        self,
        chunked_docs: List[Document],
        output_file: str
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            for doc in chunked_docs:

                record = {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                }

                file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    ) + "\n"
                )

        logger.info(
            f"Saved {len(chunked_docs)} chunks to {output_file}"
        )