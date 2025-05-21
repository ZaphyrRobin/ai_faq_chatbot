import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain.schema import Document
from db.database import get_pg_connection
from settings import COLLECTION_NAME
from typing import List

logger = logging.getLogger(__name__)

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_and_store_entries(entries: List[tuple[str, str]]):
    """
    Embeds and stores a list of (question, answer) entries into the vector store.
    """
    documents = []
    for question, content in entries:
        if content:
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "type": "content",
                        "original_question": question or ""
                    }
                )
            )

        if question:
            documents.append(
                Document(
                    page_content=question,
                    metadata={
                        "type": "question",
                        "paired_content": content or ""
                    }
                )
            )

    vectorstore = PGVector(
        connection_string=get_pg_connection(),
        embedding_function=embedding_function,
        collection_name=COLLECTION_NAME,
        use_jsonb=True,
    )
    vectorstore.add_documents(documents)
    logger.info(f"✅ Number of Documents embedded {len(documents)}.")
