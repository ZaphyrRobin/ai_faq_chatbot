import os
import logging
from llama_cpp import Llama
from db.database import get_vector_store

logger = logging.getLogger(__name__)

# Load quantized GGUF model (adjust path and threads)
model_path = os.getenv("LLM_MODEL_PATH", "./models/mistral-7b-instruct-v0.1.Q4_0.gguf")

llm = Llama(
    model_path=model_path,
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
