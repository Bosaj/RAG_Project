# RAG Project

A minimal Retrieval-Augmented Generation (RAG) service for uploading documents, processing their contents, indexing chunks, searching relevant context, and generating answers.

## Requirements

The application currently expects **Python 3.12.2 or later**, a running MongoDB instance, and the external services selected in the environment configuration. The dependency list is maintained in [`src/requirements.txt`](src/requirements.txt).

The application supports text and PDF document processing through the existing processing controller. The selected LLM, embedding backend, and vector database are configured through environment variables.

## Local installation

The application loads `.env` from its current working directory. Because the entrypoint and environment template are inside `src`, run the application from that directory.

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.exemple .env
```

Edit `src/.env` and provide the values required by your chosen setup. In particular, review the MongoDB connection settings, the generation and embedding backends, the model identifiers, and any provider API keys. The repository includes [`src/.env.exemple`](src/.env.exemple) as the starting template. Do not commit a real `.env` file or any secret key.

## Optional Ollama setup

If the environment is configured to use Ollama, install Ollama by following its [official installation guide](https://github.com/ollama/ollama/tree/main#ollama), download a supported model, and start the local server.

```bash
ollama pull dolphin-phi
ollama serve
```

The required model and host settings still need to be configured in `src/.env`. Refer to Ollama’s [API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) for additional server options.

## Run the FastAPI server

From the repository root:

```bash
cd src
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The base endpoint is:

```text
GET http://localhost:5000/api/v1/
```

A lightweight liveness endpoint is available for container or platform probes:

```bash
curl --fail-with-body http://localhost:5000/api/v1/health
```

It returns `{"status": "ok"}` when the FastAPI process is responding. It does not claim that MongoDB, the vector database, or external model providers are healthy; those dependencies are initialized separately during application startup.

FastAPI’s interactive documentation is available at [http://localhost:5000/docs](http://localhost:5000/docs) while the server is running.

## API workflow

The API uses a `project_id` to group uploaded files and their processed chunks. The examples below use project `1`; replace it with the identifier appropriate for your application.

### 1. Upload a document

The upload route accepts a multipart form upload. The current implementation returns a `file_id` that can be used in the processing request.

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/data/upload/1' \
  --form 'file=@/path/to/document.pdf'
```

### 2. Process the document

Processing extracts text, splits it into chunks, and stores the chunks. The request schema uses `file_id`, `chunk_size`, `overlap_size`, and `do_reset`.

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/data/process/1' \
  --header 'Content-Type: application/json' \
  --data '{
    "file_id": "<file_id_from_upload_response>",
    "chunk_size": 100,
    "overlap_size": 20,
    "do_reset": 1
  }'
```

If `file_id` is omitted, the application attempts to process all files associated with the project. Set `do_reset` to `1` only when existing chunks for the project should be removed before processing. The API validates that `chunk_size` is positive, `overlap_size` is non-negative and smaller than `chunk_size`, and `do_reset` is either `0` or `1`.

Search requests require non-empty text and accept a result `limit` from `1` through `100`.

### 3. Index the processed chunks

After processing, push the project’s chunks into the configured vector database.

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/nlp/index/push/1' \
  --header 'Content-Type: application/json' \
  --data '{
    "do_reset": 1
  }'
```

### 4. Search the index

The search route accepts a text query and an optional result limit.

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/nlp/index/search/1' \
  --header 'Content-Type: application/json' \
  --data '{
    "text": "What is the main topic of the document?",
    "limit": 5
  }'
```

A GET form is also available:

```bash
curl --fail-with-body \
  'http://localhost:5000/api/v1/nlp/index/search/1?text=What%20is%20the%20main%20topic%3F&limit=5'
```

### 5. Generate a RAG answer

The answer route searches the indexed context and generates an answer through the configured language model.

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/nlp/index/answer/1' \
  --header 'Content-Type: application/json' \
  --data '{
    "text": "What is the main topic of the document?",
    "limit": 5
  }'
```

## Project structure

```text
src/
├── main.py                 # FastAPI application entrypoint
├── requirements.txt        # Python dependencies
├── .env.exemple            # Environment-variable template
├── controllers/            # Upload, processing, and RAG logic
├── helpers/                # Configuration helpers
├── models/                 # Database and domain models
├── routes/                 # FastAPI routers and request schemas
└── stores/                 # LLM, embedding, and vector-database providers
```

## Security and troubleshooting

Keep credentials in `src/.env` and never commit them. If the application fails during startup, first confirm that MongoDB is reachable and that all required settings in the environment file are populated. If an API request fails, check the FastAPI logs and confirm that the request follows the route and schema shown above.

## Contributing

Small, focused improvements are welcome. Before opening a pull request, describe the problem being solved, explain how the change was verified, and avoid including secrets or generated data. Documentation updates should be tested by following the commands from a clean environment whenever possible.
