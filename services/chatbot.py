import logging
from db.database import get_vector_store
from llama_cpp import Llama
from settings import LLM_MODEL_PATH

logger = logging.getLogger(__name__)

llm = Llama(
    model_path=LLM_MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

# Using PGVector
retriever = get_vector_store().as_retriever()

def get_answer(question: str) -> str:
    # Retrieve relevant documents from PGVector
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])

    # Construct prompt with both context and question
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:"""

    # Call LLM to get the output
    output = llm(prompt, max_tokens=5000)
    logger.debug(f"✅ Retriever\n{context}")
    logger.debug(f"✅ output {output}")
    return output["choices"][0]["text"].strip()
