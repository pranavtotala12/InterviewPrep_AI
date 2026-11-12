from pathlib import Path
import sys

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.search_service import retrieve_relevant_chunks

if __name__ == "__main__":
    test_queries = [
        "What is delegation in Canvas apps?",
        "Explain Microsoft Dataverse security and business units.",
    ]

    for question in test_queries:
        print("=" * 60)
        print(f"QUERY: {question}")
        print("=" * 60)

        results = retrieve_relevant_chunks(question, top_k=2)

        for rank, item in enumerate(results, start=1):
            source = item["metadata"].get("source", "Unknown")
            page = item["metadata"].get("page_number", "Unknown")
            score = item["score"]

            print(f"\n[Rank {rank}] Similarity Score: {score:.4f}")
            print(f"Source: {source} (Page {page})")
            print("Content Snippet:")
            print(item["content"][:300].strip())
            print("...\n")