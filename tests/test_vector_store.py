import os
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.chunking_service import chunk_text
from app.services.embedding_service import get_embeddings_batch
from app.services.pdf_service import extract_text_from_pdf
from app.services.vector_store import add_chunks_to_vector_store, get_record_count

if __name__ == "__main__":
    pdf_path = "data/pdfs/Power Platform Interview Preparation Guide.pdf"

    print("1. Extracting PDF text...")
    pages = extract_text_from_pdf(pdf_path)
    print(f"   Extracted {len(pages)} pages.")

    print("2. Chunking text...")
    chunks = chunk_text(pages, chunk_size=500, chunk_overlap=100)
    print(f"   Generated {len(chunks)} chunks.")

    print("3. Generating embeddings for chunks...")
    chunk_texts = [c["content"] for c in chunks]

    batch_size = 10
    all_embeddings = []

    for i in range(0, len(chunk_texts), batch_size):
        batch = chunk_texts[i : i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(chunk_texts) + batch_size - 1) // batch_size
        print(f"   Embedding batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        embeddings = get_embeddings_batch(batch)
        all_embeddings.extend(embeddings)
        time.sleep(0.5)

    print(f"\nVerification: {len(chunks)} chunks vs {len(all_embeddings)} embeddings.")

    print("4. Storing vectors and metadata in PostgreSQL (pgvector)...")
    add_chunks_to_vector_store(chunks, all_embeddings)

    print(f"\nSuccess! Total records stored in PostgreSQL: {get_record_count()}")