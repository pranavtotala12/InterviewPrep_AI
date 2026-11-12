from pathlib import Path
import sys

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.pdf_service import extract_text_from_pdf

if __name__ == "__main__":
    # Ensure this matches the exact folder name where you placed the file
    sample_pdf_path = "data/pdfs/Power Platform Interview Preparation Guide.pdf"

    try:
        pages = extract_text_from_pdf(sample_pdf_path)
        print("Extraction Successful!")
        print(f"Total pages extracted: {len(pages)}\n")

        if pages:
            first_page = pages[0]
            print(
                f"--- Document: {first_page['source']} | Page: {first_page['page_number']} ---"
            )
            print("Content Preview (first 300 characters):")
            print(first_page["content"][:300])
            print("\n...")

    except FileNotFoundError as err:
        print(f"File Error: {err}")