import logging
from langchain_postgres.vectorstores import PGVector
from settings import COLLECTION_NAME
from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy import text
from utils.embedding import get_embedding_function

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
    return PGVector(
        connection=DATABASE_URL,
        collection_name=COLLECTION_NAME,
        embeddings=get_embedding_function(),
        use_jsonb=True,
    )

def clear_all_embeddings():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM langchain_pg_embedding"))
        conn.commit()
        logging.info("✅ All embeddings deleted from langchain_pg_embedding.")
