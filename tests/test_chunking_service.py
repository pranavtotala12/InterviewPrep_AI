from pathlib import Path
import sys

# Ensure project root is in python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.chunking_service import chunk_text
from app.services.pdf_service import extract_text_from_pdf

if __name__ == "__main__":
    pdf_path = "data/pdfs/Power Platform Interview Preparation Guide.pdf"

    # 1. Extract raw pages
    pages = extract_text_from_pdf(pdf_path)
    print(f"Total Pages Extracted: {len(pages)}")

    # 2. Chunk pages
    chunks = chunk_text(pages, chunk_size=500, chunk_overlap=100)
    print(f"Total Chunks Generated: {len(chunks)}\n")

    # 3. Inspect the first two chunks to verify overlap
    if len(chunks) >= 2:
        print("=== CHUNK 0 ===")
        print(f"ID: {chunks[0]['chunk_id']}")
        print(f"Metadata: {chunks[0]['metadata']}")
        print(f"Content:\n{chunks[0]['content']}\n")

        print("=== CHUNK 1 ===")
        print(f"ID: {chunks[1]['chunk_id']}")
        print(f"Metadata: {chunks[1]['metadata']}")
        print(f"Content:\n{chunks[1]['content']}\n")