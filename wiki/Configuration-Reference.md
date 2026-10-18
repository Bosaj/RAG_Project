# Configuration Reference

RAG Project uses Pydantic Settings to load environment variables from `.env` in the process working directory. The canonical names and types are defined in [`src/helpers/config.py`](https://github.com/Bosaj/RAG_Project/blob/main/src/helpers/config.py); the repository template is [`src/.env.exemple`](https://github.com/Bosaj/RAG_Project/blob/main/src/.env.exemple).

> Run the service from `src` so `env_file = ".env"` resolves to `src/.env`.

## Application and upload settings

| Variable | Type | Description |
|---|---:|---|
| `APP_NAME` | string | Application name used by the runtime configuration. |
| `APP_VERSION` | string | Application version string. |
| `FILE_ALLOWED_TYPES` | list | Accepted MIME types. The repository template uses `text/plain` and `application/pdf`. |
| `FILE_MAX_SIZE` | integer | Maximum upload size according to the controller’s configured size unit. Verify the intended unit before changing production limits. |
| `FILE_DEFAULT_CHUNK_SIZE` | integer | Number of bytes read per asynchronous upload iteration. |

The upload controller validates MIME type and known file size before writing the file. A streaming request with an unknown size is allowed to proceed through chunked reading, while a known oversized file is rejected.

## MongoDB settings

| Variable | Type | Example | Description |
|---|---:|---|---|
| `MONGODB_URL` | string | `mongodb://localhost:27017` | MongoDB connection URL. |
| `MONGODB_DATABASE` | string | `rag_db` | Database name used by project, asset, and chunk models. |

For the included Docker Compose setup, MongoDB is exposed on host port `27007`, so a credentialed URL may resemble:

```text
mongodb://<username>:<password>@localhost:27007/?authSource=admin
```

Use URL encoding for credentials containing reserved URI characters.

## LLM and embedding settings

| Variable | Type | Description |
|---|---:|---|
| `GENERATION_BACKEND` | string | Generation provider name selected by `LLMProviderFactory`. |
| `EMBEDDING_BACKEND` | string | Embedding provider name selected by `LLMProviderFactory`. |
| `GENERATION_MODEL_ID` | string | Model identifier used by the generation client. |
| `EMBEDDING_MODEL_ID` | string | Model identifier used by the embedding client. |
| `EMBEDDING_MODEL_SIZE` | integer | Expected embedding vector dimension. |
| `INPUT_DAFAULT_MAX_CHARACTERS` | integer | Maximum input-character setting used by provider configuration. The misspelling is part of the existing public configuration name. |
| `GENERATION_DAFAULT_MAX_TOKENS` | integer | Maximum generated-token setting used by provider configuration. The misspelling is part of the existing public configuration name. |
| `GENERATION_DAFAULT_TEMPERATURE` | float | Generation temperature. |

Provider credentials and URLs are optional at schema level but become required when the selected provider needs them:

| Variable | Used by |
|---|---|
| `OPENAI_API_KEY` | OpenAI generation or embedding integrations. |
| `OPENAI_BASE_URL` | Optional OpenAI-compatible endpoint override. |
| `COHERE_API_KEY` | Cohere integration. |
| `GEMINI_API_KEY` | Gemini integration. |

The provider factory currently exposes OpenAI, Cohere, Gemini, Local, and Ollama paths according to the implementation. The exact provider capability depends on the selected provider class; confirm the class before using a backend for both generation and embeddings.

## Vector database settings

| Variable | Type | Example | Description |
|---|---:|---|---|
| `VECTOR_DB_BACKEND` | string | `QDRANT` | Vector database provider name. The current factory supports `QDRANT`. |
| `VECTOR_DB_PATH` | string | `qdrant_db` | Database path passed through the storage-root helper. |
| `VECTOR_DB_DISTANCE_METHOD` | string | `cosine` | Distance method passed to the Qdrant provider. The enum defines `cosine` and `dot`. |

Unsupported vector provider names raise an actionable `ValueError` during factory creation instead of returning `None` and failing later with an unrelated attribute error.

## Language and prompt settings

| Variable | Type | Default | Description |
|---|---:|---:|---|
| `PRIMARY_LANG` | string | `en` | Preferred locale used by `TemplateParser`. |
| `DEFAULT_LANG` | string | `en` | Fallback locale when the preferred template is unavailable. |

Prompt templates are stored under `src/stores/llm/templates/locales/<language>/`. The parser falls back to the default language when a requested locale or template group is unavailable.

## Example development configuration

The following is a starting point only. Replace placeholder credentials and model identifiers with values supported by the selected providers:

```dotenv
APP_NAME="RAG"
APP_VERSION="0.1"
FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000

MONGODB_URL="mongodb://localhost:27017"
MONGODB_DATABASE="rag_db"

GENERATION_BACKEND="GEMINI"
EMBEDDING_BACKEND="LOCAL"
GEMINI_API_KEY="replace-me"
GENERATION_MODEL_ID="gemini-pro"
EMBEDDING_MODEL_ID="text-embedding-3-small"
EMBEDDING_MODEL_SIZE=1536
INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=200
GENERATION_DAFAULT_TEMPERATURE=0.1

VECTOR_DB_BACKEND="QDRANT"
VECTOR_DB_PATH="qdrant_db"
VECTOR_DB_DISTANCE_METHOD="cosine"

PRIMARY_LANG="en"
DEFAULT_LANG="en"
```

Do not copy real keys into this page, the repository, issue comments, pull requests, logs, or screenshots. If a credential is exposed, revoke it immediately and replace it with a new secret.
