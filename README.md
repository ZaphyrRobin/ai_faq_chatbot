# 📚 Local AI RAG-based FAQ Chatbot

A blazing-fast, fully local, and open-source chatbot support both CI and Web UI, powered by:

- ⚡ [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) for LLM inference (e.g., Mistral-7B GGUF)
- 🧠 [`sentence-transformers`](https://www.sbert.net/) for embedding generation
- 🗃️ PostgreSQL + [`pgvector`](https://github.com/pgvector/pgvector) for semantic vector search
- 🕸️ Web crawling [FAQ] (https://makersplace.com/faq/) as domain knowledge
- ⚛️ Frontend (React.js, Vite)

---

## 🧩 Medium blog
- [Medium blog to cover this](https://medium.com/@chongyao.robin/transform-a-static-faq-page-into-a-rag-based-ai-chatbot-458febe8ebcb)

---

## 📋 Features

- Fully local and private — no external API calls
- Embeds any webpage or FAQ using `BeautifulSoup`
- Answers questions by retrieving the most relevant context chunks
- Supports CLI-based Q&A
- Simple Web UI

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
CREATE USER <db_username> WITH PASSWORD <db_passport>;
CREATE DATABASE chatbot OWNER <db_username>;
\q
```

Update the metadata column to JSONB for better performance:
```
ALTER TABLE langchain_pg_embedding
ALTER COLUMN cmetadata TYPE JSONB USING cmetadata::jsonb;
```

export your DATABASE_URL:
```
cd backend
export DATABASE_URL="postgresql+psycopg2://<db_username>:<db_passport>@localhost:5432/chatbot"
```

### 4. Download an LLM Model
Download a quantized .gguf model from HuggingFace, e.g.:
```
cd backend
mkdir -p models/
mv mistral-7b-instruct-v0.1.Q4_0.gguf models/

# Optional
export LLM_MODEL_PATH="./models/mistral-7b-instruct-v0.1.Q4_0.gguf"
```

### 5. Install and run Redis
```
brew install redis
brew services start redis
```

### 6. Install frontend packages and run frontend
```
cd frontend
npm install
npm run dev
```

### 7. Run backend server
```
cd backend
python3 -m uvicorn main:app --reload
```

### 8. Local Urls
Visit backend API docs: http://localhost:8000/docs

Visit frontend React UI: http://localhost:5173/

### 9. Sum up - to start web UI

NOTE: If you like to use different url, please adjust the web crawler logic at utils/web_crawler.py

```
cd backend
brew services start redis
export DATABASE_URL="postgresql+psycopg2://<db_username>:<db_passport>@localhost:5432/chatbot"
python3 main.py -v -u "https://makersplace.com/faq/" -q "What is bitcoin?"
python3 -m uvicorn main:app --reload

cd frontend
npm run dev
```
Web UI at: http://localhost:5173/

### 10. [Optional] CLI Commands
```
# -v meaning enabled logging in INFO level
# -u the page url that the web crawler starts from. Split in comma if multiple urls
# -q the question string
cd backend
python3 main.py -v -u "https://makersplace.com/faq/" -q "What is bitcoin?"

...
2025-05-21 08:30:25 [INFO] root: ✅ All embeddings deleted from langchain_pg_embedding.
2025-05-21 08:30:26 [INFO] httpx: HTTP Request: GET https://makersplace.com/faq/ "HTTP/1.1 200 OK"
2025-05-21 09:28:39 [INFO] utils.web_crawler: ✅ Fetched 82 entries.
2025-05-21 09:28:39 [INFO] sentence_transformers.SentenceTransformer: Use pytorch device_name: mps
2025-05-21 09:28:39 [INFO] sentence_transformers.SentenceTransformer: Load pretrained SentenceTransformer: sentence-transformers/all-MiniLM-L6-v2
2025-05-21 09:28:40 [INFO] services.embedder: ✅ Number of Documents embedded 164.
2025-05-21 08:30:37 [INFO] __main__: 
Question: What is bitcoin? 

Answer: Bitcoin is a cryptocurrency that operates independently of a central bank. It is decentralized and is based on blockchain technology. It allows peer-to-peer transactions and is considered a digital form of gold. Unlike Ethereum, Bitcoin does not have a fee to interact with it, but instead relies on a consensus mechanism called proof-of-work to validate transactions.
```

## 🔮 Future Improvements
1. Improve prompt formatting and relevance handling
2. Support multiple LLM models and quantizations
3. Add automated tests and evaluation scripts
4. Dockerize for local and cloud deployment


## 📝 License
MIT License
