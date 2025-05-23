import logging
from db.database import get_vector_store
from langchain_core.documents import Document
from typing import List

logger = logging.getLogger(__name__)

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

    vectorstore = get_vector_store()
    vectorstore.add_documents(documents)
    logger.info(f"✅ Number of Documents embedded {len(documents)}.")
