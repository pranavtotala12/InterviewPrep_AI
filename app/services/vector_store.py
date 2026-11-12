import json
import os
from typing import Any, Dict, List
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "768"))

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file.")


def get_connection():
    """Establishes connection to PostgreSQL and registers pgvector support."""
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    return conn


def init_vector_table(dimension: int = EMBEDDING_DIMENSION):
    """Enables the pgvector extension and creates the document chunks table."""
    # Step 1: Raw connection without register_vector to enable the extension first
    raw_conn = psycopg2.connect(DATABASE_URL)
    try:
        with raw_conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        raw_conn.commit()
    finally:
        raw_conn.close()

    # Step 2: Now that the vector type exists in Postgres, connect with register_vector
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB,
                    embedding vector({dimension})
                );
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_embedding 
                ON document_chunks 
                USING hnsw (embedding vector_cosine_ops);
            """)
        conn.commit()
    finally:
        conn.close()


def add_chunks_to_vector_store(
    chunks: List[Dict[str, Any]], embeddings: List[List[float]]
):
    """Upserts document chunks, metadata, and embeddings into PostgreSQL."""
    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk/Embedding count mismatch: received {len(chunks)} chunks and {len(embeddings)} embeddings."
        )

    # Initialize the extension and schema
    dimension = len(embeddings[0]) if embeddings else EMBEDDING_DIMENSION
    init_vector_table(dimension=dimension)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO document_chunks (chunk_id, content, metadata, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    content = EXCLUDED.content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding;
            """
            for chunk, emb in zip(chunks, embeddings):
                cur.execute(
                    query,
                    (
                        chunk["chunk_id"],
                        chunk["content"],
                        json.dumps(chunk["metadata"]),
                        emb,
                    ),
                )
        conn.commit()
    finally:
        conn.close()


def search_vector_store(
    query_vector: List[float], top_k: int = 3
) -> List[Dict[str, Any]]:
    """Performs cosine distance similarity search using the <=> operator."""
    conn = get_connection()
    results = []
    # Convert Python list to pgvector string format '[0.1, 0.2, ...]'
    vector_str = str(query_vector)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_id, content, metadata, 1 - (embedding <=> %s::vector) AS similarity
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (vector_str, vector_str, top_k),
            )

            rows = cur.fetchall()
            for row in rows:
                results.append(
                    {
                        "chunk_id": row[0],
                        "content": row[1],
                        "metadata": row[2],
                        "score": float(row[3]),
                    }
                )
    finally:
        conn.close()
    return results


def get_record_count() -> int:
    """Returns the total number of document chunks indexed."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM document_chunks;")
            return cur.fetchone()[0]
    finally:
        conn.close()