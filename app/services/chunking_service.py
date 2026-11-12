from typing import Any, Dict, List


def chunk_text(
    pages: List[Dict[str, Any]], chunk_size: int = 500, chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """Splits extracted page text into overlapping chunks while preserving metadata.

    Args:
        pages: List of dicts containing 'page_number', 'content', and 'source'.
        chunk_size: Approximate size of each chunk in characters.
        chunk_overlap: Number of characters to overlap between adjacent chunks.

    Returns:
        List of dicts representing chunk items with text and metadata.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size")

    chunks = []
    chunk_index = 0

    for page_data in pages:
        content = page_data["content"]
        page_number = page_data["page_number"]
        source = page_data["source"]

        start = 0
        text_length = len(content)

        while start < text_length:
            end = start + chunk_size
            chunk_content = content[start:end].strip()

            if chunk_content:
                chunks.append(
                    {
                        "chunk_id": f"{source}_p{page_number}_c{chunk_index}",
                        "content": chunk_content,
                        "metadata": {
                            "source": source,
                            "page_number": page_number,
                            "chunk_index": chunk_index,
                        },
                    }
                )
                chunk_index += 1

            # Move forward by (chunk_size - chunk_overlap)
            start += chunk_size - chunk_overlap

    return chunks