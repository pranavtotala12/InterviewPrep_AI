from pathlib import Path
from typing import Any, Dict, List
import pymupdf as fitz  # PyMuPDF is imported as 'fitz'


def extract_text_from_pdf(file_path: str) -> List[Dict[str, Any]]:
    """Opens a PDF file and extracts text page by page with metadata."""
    path = Path(file_path)

    # 1. Check if the file actually exists
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    extracted_pages = []

    # 2. Open the PDF document using PyMuPDF
    with fitz.open(file_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()

            # Clean whitespace
            cleaned_text = text.strip()

            # 3. Only keep pages that contain text
            if cleaned_text:
                extracted_pages.append(
                    {
                        "page_number": page_num + 1,  # 1-indexed for readability
                        "content": cleaned_text,
                        "source": path.name,
                    }
                )

    return extracted_pages