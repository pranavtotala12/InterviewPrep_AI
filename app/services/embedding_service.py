import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "768"))

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=API_KEY)


def get_embedding(text: str) -> List[float]:
    """Generates a vector embedding for a single text chunk with configured dimensionality."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSION),
    )
    return response.embeddings[0].values


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generates vector embeddings for a list of strings, ensuring a 1:1 chunk-to-vector mapping."""
    embeddings = []
    for text in texts:
        embeddings.append(get_embedding(text))
    return embeddings