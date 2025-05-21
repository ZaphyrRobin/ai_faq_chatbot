import os

COLLECTION_NAME = "faq_docs"

# Load quantized GGUF model (adjust path and threads)
# Please set it if needed
# e.g export LLM_MODEL_PATH="./models/mistral-7b-instruct-v0.1.Q4_0.gguf"
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "./models/mistral-7b-instruct-v0.1.Q4_0.gguf")

# Please set it if needed
# e.g export DATABASE_URL="postgresql+psycopg2://<user>:<password>@localhost:5432/<db_name>"
DATABASE_URL = os.getenv("DATABASE_URL")
