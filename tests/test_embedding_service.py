import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.embedding_service import get_embedding, get_embeddings_batch

if __name__ == "__main__":
    sample_text = "What is delegation in Microsoft Power Apps?"
    print(f"Generating embedding for: '{sample_text}'...")

    try:
        vector = get_embedding(sample_text)
        print("Embedding generated successfully!")
        print(f"Vector Dimensions: {len(vector)}")
        print(f"Vector Preview (first 5 values): {vector[:5]}\n")

        # Batch test
        batch_samples = [
            "What is Microsoft Dataverse?",
            "Explain Power Automate cloud flows.",
        ]
        batch_vectors = get_embeddings_batch(batch_samples)
        print(f"Batch embedding generated {len(batch_vectors)} vectors successfully.")

    except Exception as e:
        print(f"Error during embedding generation: {e}")