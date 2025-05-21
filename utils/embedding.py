from langchain_huggingface import HuggingFaceEmbeddings
from settings import EMBEDDING_MODEL_NAME

def get_embedding_function():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
