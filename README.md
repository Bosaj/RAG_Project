# 🧠 RAG Project — Production-Ready Retrieval-Augmented Generation Engine

[![CI Tests](https://github.com/Bosaj/RAG_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Bosaj/RAG_Project/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-red.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Metadata%20Store-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A high-performance, modular **Retrieval-Augmented Generation (RAG)** backend engine built with **FastAPI**, **Qdrant**, and **MongoDB**. Supports multi-provider LLMs (OpenAI, Google Gemini, Cohere, Ollama), multi-format document ingestion (PDF, TXT), multilingual prompt templates, and isolated project namespaces.

---

## 🏗️ Architecture & Pipeline

`mermaid
graph TD
    subgraph "1. Ingestion Layer"
        DOC["📄 Upload Documents (PDF / TXT)"] --> VAL["🛡️ Path & Size Validation"]
        VAL --> STOR["💾 Project Storage Root"]
    end

    subgraph "2. Processing & Indexing"
        STOR --> CHUNK["✂️ Text Splitter (Chunk & Overlap)"]
        CHUNK --> EMB["🔢 Embedding Engine (OpenAI / Gemini / Cohere / Local)"]
        EMB --> VEC["🎯 Qdrant Vector DB (Indexed Chunks)"]
        CHUNK --> META["🗄️ MongoDB (Document & Project Metadata)"]
    end

    subgraph "3. Query & Generation"
        USER["👤 User Query"] --> RET["🔍 Vector Similarity Search (Top-K Chunks)"]
        VEC --> RET
        RET --> PROMPT["📝 Multilingual Prompt Assembly (EN / AR)"]
        PROMPT --> LLM["🤖 LLM Provider (OpenAI / Gemini / Cohere / Ollama)"]
        LLM --> RESP["💬 Context-Grounded Answer"]
    end
`

---

## ✨ Key Features

- **🚀 High-Performance Async Backend**: Built with FastAPI for ultra-low latency API endpoints and non-blocking I/O.
- **📁 Multi-Tenant Project Isolation**: Automatic project scoping (project_id) ensures strict separation of documents and embeddings.
- **🧩 Pluggable Vector DB**: Out-of-the-box integration with **Qdrant Vector Database** via unified VectorDBInterface.
- **🤖 Multi-Provider LLM & Embeddings**: Seamlessly switch between **OpenAI**, **Google Gemini**, **Cohere**, and **Ollama** (Local LLM) via configuration.
- **🌍 Multilingual Prompt Engine**: Native multi-locale prompt templates (English & Arabic) with pluggable template parsers.
- **🛡️ Enterprise Security**: Path-traversal protection, strict filename sanitization, upload size controls, and automated secret scanning.
- **🧪 Comprehensive Test Suite**: 100% automated test coverage with GitHub Actions CI across Python 3.10, 3.11, and 3.12.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com) | High-speed REST API & OpenAPI docs |
| **Vector Database** | [Qdrant](https://qdrant.tech) | High-dimensional vector indexing & similarity search |
| **Metadata Database** | [MongoDB](https://www.mongodb.com) | Document metadata and project tracking |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev) | Schema enforcement & settings management |
| **Document Processing** | [LangChain](https://www.langchain.com) / PyMuPDF | Text extraction, tokenization & chunking |
| **Testing & CI** | [pytest](https://pytest.org) + GitHub Actions | Automated regression and multi-Python matrix testing |

---

## 🚀 Quick Start

### 1. Clone the Repository
\\\ash
git clone https://github.com/Bosaj/RAG_Project.git
cd RAG_Project
\\\

### 2. Configure Environment Variables
\\\ash
cd src
cp .env.exemple .env
# Edit .env with your MongoDB URL, Vector DB path, and chosen LLM API keys
\\\

### 3. Start MongoDB with Docker Compose
\\\ash
# From the repository root:
cp docker/.env.example docker/.env
docker compose --env-file docker/.env -f docker/docker.compose.yml up -d mongodb
\\\

### 4. Run the FastAPI Application
\\\ash
cd src
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 5000
\\\

Interactive OpenAPI Swagger docs will be available at: **[http://localhost:5000/docs](http://localhost:5000/docs)**

---

## 📡 REST API Reference

### Health & Liveness
\\\ash
curl -X GET http://localhost:5000/api/v1/health
# Response: {"status": "ok"}
\\\

### 1. Upload a Document
\\\ash
curl -X POST 'http://localhost:5000/api/v1/data/upload/project_1' \
  -F 'file=@sample_document.pdf'
\\\

### 2. Process & Index Document Chunks
\\\ash
curl -X POST 'http://localhost:5000/api/v1/process/project_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "file_id": "sample_document.pdf",
    "chunk_size": 400,
    "overlap_size": 40,
    "do_reset": false
  }'
\\\

### 3. Search Relevant Context
\\\ash
curl -X POST 'http://localhost:5000/api/v1/nlp/search/project_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "What are the key findings of the report?",
    "limit": 5
  }'
\\\

### 4. Query RAG Answer Generation
\\\ash
curl -X POST 'http://localhost:5000/api/v1/nlp/answer/project_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Summarize the key conclusions from the uploaded document.",
    "language": "en"
  }'
\\\

---

## 🧪 Testing & Quality Assurance

Run the test suite across all controllers, schema validators, and provider factories:

\\\ash
# Run pytest with src added to PYTHONPATH
PYTHONPATH=src pytest -v
\\\

---

## 🤝 Contributing & Community

Contributions are what make the open source community such an amazing place to learn, inspire, and create.
- Please review our **[Contributing Guidelines](CONTRIBUTING.md)**.
- Read our **[Code of Conduct](CODE_OF_CONDUCT.md)**.
- Report security issues following our **[Security Policy](SECURITY.md)**.

---

## 📄 License

Distributed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for more information.

---

**Developed with ❤️ by [Bosaj (Oussama EL HADJI)](https://github.com/Bosaj)**
