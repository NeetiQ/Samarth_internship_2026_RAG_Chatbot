import json
from sentence_transformers import SentenceTransformer


INPUT_FILE = "chunked_documents.jsonl"
OUTPUT_FILE = "embedded_documents.jsonl"

MODEL_NAME = "BAAI/bge-small-en-v1.5"
BATCH_SIZE = 32


def load_chunks():
    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)

            text = record.get("page_content", "").strip()

            if text:
                records.append(record)

    return records


def main():
    print("Loading chunks...")

    records = load_chunks()

    print(f"Total chunks found: {len(records)}")

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        record["page_content"]
        for record in records
    ]

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print("Saving embeddings...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for record, embedding in zip(records, embeddings):
            output_record = {
                "page_content": record["page_content"],
                "metadata": record["metadata"],
                "embedding": embedding.tolist(),
            }

            file.write(
                json.dumps(output_record, ensure_ascii=False) + "\n"
            )

    print("Done.")
    print(f"Saved file: {OUTPUT_FILE}")
    print(f"Embedding size: {len(embeddings[0])}")


if __name__ == "__main__":
    main()