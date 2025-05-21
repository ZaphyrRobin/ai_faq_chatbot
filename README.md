# 📚 Local AI RAG-based FAQ Chatbot

A blazing-fast, fully local, and open-source chatbot CLI powered by:

- ⚡ [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) for LLM inference (e.g., Mistral-7B GGUF)
- 🧠 [`sentence-transformers`](https://www.sbert.net/) for embedding generation
- 🗃️ PostgreSQL + [`pgvector`](https://github.com/pgvector/pgvector) for semantic vector search

---

## 📋 Features

- Fully local and private — no external API calls
- Embeds any webpage or FAQ using `BeautifulSoup`
- Answers questions by retrieving the most relevant context chunks
- Supports CLI-based Q&A and is extensible to FastAPI

---

## 📦 Requirements

- Python 3.8+
- PostgreSQL with `pgvector` extension
- A quantized `.gguf` LLM model (e.g., Mistral-7B)

---

## 🚀 Getting Started

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/your-username/local-chatbot.git
cd local-chatbot
pip install -r requirements.txt
```

### 2. Install PostgreSQL + pgvector
```
brew update
brew install postgresql
brew install pgvector
brew services start postgresql
```

Enable pgvector in your PostgreSQL DB:
```
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3. Configure the Database
Set up your database (if not already created):
```
# Example: create user + db manually
psql -U postgres

-- In psql
CREATE USER chatbot_user WITH PASSWORD 'chatbotai';
CREATE DATABASE chatbot OWNER chatbot_user;
\q
```

Update the metadata column to JSONB for better performance:
```
ALTER TABLE langchain_pg_embedding
ALTER COLUMN metadata TYPE JSONB USING metadata::jsonb;
```

export your DATABASE_URL:
```
export DATABASE_URL="postgresql+psycopg2://chatbot_user:chatbotai@localhost:5432/chatbot"
```

### 4. Download an LLM Model
Download a quantized .gguf model from HuggingFace, e.g.:
```
mkdir -p models/
mv mistral-7b-instruct-v0.1.Q4_0.gguf models/
export LLM_MODEL_PATH="./models/mistral-7b-instruct-v0.1.Q4_0.gguf"
```

### 5. CLI Examples
```
# -v meaning enabled logging in INFO level
# -u the page url that the web crawler starts from. Split in comma if multiple urls
# -q the question string
python3 main.py -v -u "https://makersplace.com/faq/" -q "What is MakersPlace?"
```

## 🔮 Future Improvements
1. Add FastAPI endpoint for web/API access
2. Improve prompt formatting and relevance handling
3. Support multiple LLM models and quantizations
4. Add caching (documents, context, LLM outputs)
5. Enable incremental embedding (only embed updated content)
7. Build simple Web UI with Streamlit or React
8. Support metadata filters in search (e.g., by source or tags)
9. Add automated tests and evaluation scripts
10. Dockerize for local and cloud deployment


## 📝 License
MIT License
