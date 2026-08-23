# RAG Project — FastAPI Retrieval-Augmented Generation Engine

Modular RAG backend: upload documents, chunk and embed them, index into Qdrant, and answer questions grounded in the retrieved context.

[![CI Tests](https://github.com/Bosaj/RAG_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Bosaj/RAG_Project/actions/workflows/ci.yml)
[![Python checks](https://github.com/Bosaj/RAG_Project/actions/workflows/python-checks.yml/badge.svg)](https://github.com/Bosaj/RAG_Project/actions/workflows/python-checks.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-red.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Origin & Attribution

This project was originally forked from [Abdelilah04116/RAG_Project](https://github.com/Abdelilah04116/RAG_Project), which provided the initial FastAPI boilerplate: the project/asset/chunk MongoDB models, the upload → chunk → embed → search flow, the LLM/vector-DB provider factories, and Docker/MongoDB scaffolding.

Since forking, **Oussama EL HADJI (Bosaj)** has extended it with:

- **Security hardening**: path-traversal protection and canonical path resolution for uploaded/processed files, upload filename sanitization, upload-size and chunk-parameter validation, cleanup of failed uploads.
- **CI/CD**: two GitHub Actions workflows running the test suite across Python 3.10, 3.11, and 3.12.
- **Settings migration** from Pydantic v1 style to Pydantic v2 `SettingsConfigDict`.
- **A pluggable LanceDB vector-store provider** as an alternative to Qdrant.
- **French RAG prompt templates**, in addition to the existing English/Arabic locales.
- **Project infrastructure**: `pyproject.toml`, `Makefile`, a Dockerfile, and a Qdrant service in Docker Compose.
- **Test coverage** for controllers, schemas, provider factories, and prompt templates.
- **Repository health files**: Code of Conduct, expanded Contributing/Security guidelines, issue templates, and a PR template.
- Sample datasets (`data/eniadproject/`) used for local, offline testing of the ingestion pipeline.

The core request/response flow, MongoDB data models, and the original LLM/vector-DB provider abstractions are inherited from the upstream project. Full commit-level history for both is in `git log`.

## Overview

`RAG_Project` is a FastAPI service implementing a full retrieval-augmented generation pipeline:

1. A client uploads a document (PDF or TXT) to a project.
2. The document is split into overlapping text chunks and the chunks are stored as metadata in MongoDB.
3. The chunks are embedded and pushed into a per-project Qdrant (or LanceDB) collection.
4. A query is embedded, the closest chunks are retrieved by vector similarity, and an LLM generates an answer grounded in those chunks, using a language-specific prompt template (English, French, or Arabic).

Each project is identified by a `project_id` and gets its own storage directory, MongoDB records, and vector-DB collection, so multiple document sets can be indexed and queried independently from the same running service.

## Features

- **Async FastAPI backend** with an OpenAPI/Swagger UI at `/docs`.
- **Per-project isolation**: uploads, chunks, and vector collections are scoped by `project_id`.
- **Pluggable vector store**: Qdrant by default, LanceDB as an alternative, behind a common `VectorDBInterface`.
- **Pluggable LLM/embedding backends**: OpenAI, Google Gemini, Cohere, Ollama (local), and a local `sentence-transformers` embedding provider — selected purely through environment variables.
- **Multilingual prompt templates**: English, French, and Arabic RAG prompts via a template parser with per-language fallback.
- **Upload and processing safeguards**: file-type/size checks, canonical path validation against the project's storage root, filename sanitization, and chunk-size/overlap validation.
- **Automated tests and CI** covering controllers, request schemas, provider factories, and templates across three Python versions.

## Architecture

```
Upload (PDF/TXT)
      │  path & size validation, unique file naming
      ▼
Project storage (disk) + Asset record (MongoDB)
      │  RecursiveCharacterTextSplitter (chunk_size / overlap_size)
      ▼
DataChunk records (MongoDB)
      │  embedding_client.embed_text(...)
      ▼
Vector store — Qdrant (default) or LanceDB, one collection per project
      │  ◄── query embedding + similarity search (top-k)
      ▼
Retrieved chunks → language-specific prompt template (en / fr / ar)
      ▼
LLM generation client (OpenAI / Gemini / Cohere / Ollama)
      ▼
Grounded answer + the assembled prompt + chat history
```

Source layout for this pipeline:

- `src/controllers/DataController.py`, `ProcessController.py` — upload validation and chunking (`langchain_text_splitters.RecursiveCharacterTextSplitter`, `PyMuPDFLoader`/`TextLoader`).
- `src/models/` — MongoDB-backed `ProjectModel`, `AssetModel`, `ChunkModel` and their `db_schemes`.
- `src/stores/vectordb/providers/` — `QdrantDBProvider` and `LanceDBProvider` behind `VectorDBInterface`.
- `src/stores/llm/providers/` — `OpenAIProvider`, `GeminiProvider`, `CoHereProvider`, `OllamaProvider`, `LocalEmbeddingProvider`.
- `src/stores/llm/templates/locales/{en,fr,ar}/rag.py` — per-language system/document/footer prompt templates.
- `src/controllers/NLPController.py` — indexing, vector search, and RAG answer assembly.

Note on Qdrant: by default the app talks to Qdrant in its embedded, on-disk mode (`QdrantClient(path=VECTOR_DB_PATH)`), so no server is required to run locally. `docker/docker.compose.yml` also ships a standalone Qdrant server container (ports `6333`/`6334`) for anyone who wants to run Qdrant as its own service; the current provider does not yet read a host/URL setting to connect to it.

## Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| API framework | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn | Async REST API, OpenAPI docs |
| Vector database | [Qdrant](https://qdrant.tech) (default) / [LanceDB](https://lancedb.github.io/lancedb/) | Chunk embeddings, similarity search |
| Metadata store | [MongoDB](https://www.mongodb.com) via Motor | Projects, assets, and chunk metadata |
| Settings & validation | [Pydantic v2](https://docs.pydantic.dev) / `pydantic-settings` | Config loading, request schema validation |
| Document processing | [LangChain](https://www.langchain.com) text splitters, PyMuPDF | PDF/TXT loading and chunking |
| LLM / embedding providers | OpenAI, Google Gemini, Cohere, Ollama, `sentence-transformers` | Generation and embedding backends |
| Testing & CI | pytest, `unittest`, GitHub Actions | Automated tests on Python 3.10–3.12 |

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB (local install or the provided Docker Compose service)
- No separate Qdrant server is required for local development — Qdrant runs embedded, on-disk, via `VECTOR_DB_PATH`. If you want Qdrant as a standalone service instead, use `docker/docker.compose.yml`.
- An API key for at least one LLM/embedding backend (OpenAI, Gemini, or Cohere), or Ollama running locally for fully offline use.

### 1. Clone and configure

```bash
git clone https://github.com/Bosaj/RAG_Project.git
cd RAG_Project
cd src
cp .env.exemple .env
```

Edit `src/.env` and set the variables you need. The settings recognized by `src/helpers/config.py` are:

| Variable | Purpose |
| :--- | :--- |
| `APP_NAME`, `APP_VERSION` | App metadata returned by `GET /api/v1/` |
| `MONGODB_URL`, `MONGODB_DATABASE` | MongoDB connection |
| `FILE_ALLOWED_TYPES`, `FILE_MAX_SIZE`, `FILE_DEFAULT_CHUNK_SIZE` | Upload validation limits |
| `GENERATION_BACKEND`, `EMBEDDING_BACKEND` | `OPENAI`, `COHERE`, `GEMINI`, `LOCAL`, or `OLLAMA` |
| `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `COHERE_API_KEY`, `GEMINI_API_KEY` | Provider credentials |
| `GENERATION_MODEL_ID`, `EMBEDDING_MODEL_ID`, `EMBEDDING_MODEL_SIZE` | Model selection |
| `INPUT_DAFAULT_MAX_CHARACTERS`, `GENERATION_DAFAULT_MAX_TOKENS`, `GENERATION_DAFAULT_TEMPERATURE` | Generation limits |
| `VECTOR_DB_BACKEND`, `VECTOR_DB_PATH`, `VECTOR_DB_DISTANCE_METHOD` | `QDRANT` or `LANCEDB`, on-disk path, `cosine`/`dot` |
| `PRIMARY_LANG`, `DEFAULT_LANG` | Prompt template language (`en`, `fr`, `ar`) with fallback |

### 2. Start MongoDB (Docker Compose)

```bash
# from the repository root
cp docker/.env.example docker/.env
docker compose --env-file docker/.env -f docker/docker.compose.yml up -d mongodb
```

### 3. Install dependencies and run the API

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Swagger UI: **http://localhost:5000/docs**

Or use the provided `Makefile`: `make install`, `make docker-up`, `make run`.

### 4. Example API workflow

```bash
# Liveness
curl http://localhost:5000/api/v1/health

# 1. Upload a document to project "project_1"
curl -X POST 'http://localhost:5000/api/v1/data/upload/project_1' \
  -F 'file=@sample_document.pdf'

# 2. Chunk the uploaded document(s)
curl -X POST 'http://localhost:5000/api/v1/data/process/project_1' \
  -H 'Content-Type: application/json' \
  -d '{"chunk_size": 400, "overlap_size": 40, "do_reset": 0}'

# 3. Push the chunks into the vector DB (Qdrant/LanceDB)
curl -X POST 'http://localhost:5000/api/v1/nlp/index/push/project_1' \
  -H 'Content-Type: application/json' \
  -d '{"do_reset": 0}'

# 4. Semantic search over the indexed chunks
curl -X POST 'http://localhost:5000/api/v1/nlp/index/search/project_1' \
  -H 'Content-Type: application/json' \
  -d '{"text": "What are the key findings of the report?", "limit": 5}'

# 5. Ask a question and get a grounded answer
curl -X POST 'http://localhost:5000/api/v1/nlp/index/answer/project_1' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Summarize the key conclusions from the uploaded document.", "limit": 5}'
```

## Testing / CI

```bash
PYTHONPATH=src pytest -v
# or
make test
```

Two GitHub Actions workflows run on every push/PR to `main`:

- `ci.yml` — pytest on Python 3.10 and 3.11.
- `python-checks.yml` — byte-compiles the source and runs the test suite via `unittest` on Python 3.12.

## Project Structure

```
RAG_Project/
├── src/
│   ├── main.py                  # FastAPI app, lifespan wiring for Mongo/LLM/vector clients
│   ├── routes/                  # base, data, nlp routers + request schemas
│   ├── controllers/             # upload validation, chunking, project paths
│   ├── models/                  # Mongo-backed models and db_schemes
│   └── stores/
│       ├── llm/                 # LLM provider factory, providers, prompt templates/locales
│       └── vectordb/            # Vector DB provider factory, Qdrant/LanceDB providers
├── docker/                      # Dockerfile, docker-compose (MongoDB + Qdrant), env example
├── data/eniadproject/           # sample documents for local testing
├── docs/                        # architecture, API reference, deployment notes
├── tests/                       # pytest/unittest suite
├── scripts/                     # dev scripts
├── pyproject.toml, Makefile     # packaging, dev commands
└── CHANGELOG.md
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the version history.

## License

Distributed under the **Apache License 2.0** — see [LICENSE](LICENSE).

## Author

**Oussama EL HADJI** ([@Bosaj](https://github.com/Bosaj)) — oussousselhadji@gmail.com
