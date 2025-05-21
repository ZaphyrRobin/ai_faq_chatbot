import os
import logging
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from settings import COLLECTION_NAME
from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy import text

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Run only once actually
def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()

def get_pg_connection():
    return DATABASE_URL

def get_vector_store() -> PGVector:
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=DATABASE_URL,
        embedding_function=embedding_function,
    )

def clear_all_embeddings():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM langchain_pg_embedding"))
        conn.commit()
        logging.info("✅ All embeddings deleted from langchain_pg_embedding.")
