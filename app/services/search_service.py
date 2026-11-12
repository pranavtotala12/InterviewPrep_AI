from typing import Any, Dict, List
from app.services.embedding_service import get_embedding
from app.services.vector_store import search_vector_store


def retrieve_relevant_chunks(
    query: str, top_k: int = 3
) -> List[Dict[str, Any]]:
    """Retrieves the top-k most semantically relevant chunks for a user question.

    Args:
        query: The interview question or topic string.
        top_k: Number of relevant context chunks to retrieve.

    Returns:
        List of dicts containing score, chunk content, and metadata.
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        return []

    # 1. Convert user question into a 768-dimension vector
    query_vector = get_embedding(cleaned_query)

    # 2. Query pgvector for the closest matches
    results = search_vector_store(query_vector=query_vector, top_k=top_k)

    return results