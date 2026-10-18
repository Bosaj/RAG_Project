# API Reference

The API is served under `/api/v1`. The interactive OpenAPI documentation is available at `/docs` when the service is running.

## Response conventions

Successful operations return a JSON object containing a `signal` field and operation-specific data. Validation and operational failures generally return HTTP `400` with a signal describing the failure. Exact signal values are defined in [`src/models/enums/ResponseEnums.py`](https://github.com/Bosaj/RAG_Project/blob/main/src/models/enums/ResponseEnums.py).

## Base and health endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/` | Base API response from the base router. |
| `GET` | `/api/v1/health` | Process liveness probe. Returns `{"status":"ok"}` when the FastAPI process responds. |

The health endpoint does not perform a dependency readiness check.

## Upload a document

```http
POST /api/v1/data/upload/{project_id}
Content-Type: multipart/form-data
```

The request must contain a multipart field named `file`. The route creates the project when necessary, validates the upload, writes the file under the project storage root, and records an asset in MongoDB.

Example:

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/data/upload/demo-project' \
  --form 'file=@/absolute/path/to/document.pdf'
```

Success response shape:

```json
{
  "signal": "file_upload_success",
  "file_id": "<asset-file-id>"
}
```

Common failure signals include an unsupported file type, an oversized file, and an upload write failure. The route removes a partially written file when the write operation raises an exception.

## Process documents

```http
POST /api/v1/data/process/{project_id}
Content-Type: application/json
```

Request body:

| Field | Type | Default | Constraints |
|---|---:|---:|---|
| `file_id` | string or null | `null` | When provided, process only that project asset. When omitted, process all project files. |
| `chunk_size` | integer | `100` | Must be greater than zero. |
| `overlap_size` | integer | `20` | Must be non-negative and strictly smaller than `chunk_size`. |
| `do_reset` | integer | `0` | Must be `0` or `1`; when `1`, delete existing project chunks before processing. |

Example:

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/data/process/demo-project' \
  --header 'Content-Type: application/json' \
  --data '{
    "file_id": "<file_id>",
    "chunk_size": 100,
    "overlap_size": 20,
    "do_reset": 1
  }'
```

Success response shape:

```json
{
  "signal": "file_processing_success",
  "inserted_chunks": 12,
  "processed_files": 1
}
```

If the requested file does not exist in the project, no files are available, a document cannot be loaded, or chunking fails, the route returns a `400` response with an appropriate processing signal.

## Push project chunks to the vector database

```http
POST /api/v1/nlp/index/push/{project_id}
Content-Type: application/json
```

Request body:

| Field | Type | Default | Constraints |
|---|---:|---:|---|
| `do_reset` | integer | `0` | Must be `0` or `1`; when `1`, reset only the first indexing page. |

Example:

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/nlp/index/push/demo-project' \
  --header 'Content-Type: application/json' \
  --data '{"do_reset": 1}'
```

Success response shape:

```json
{
  "signal": "insert_into_vectordb_success",
  "inserted_items_count": 12
}
```

The route reads chunks in pages and preserves vectors inserted by earlier pages. A vector insertion failure returns HTTP `400` with the vector-database error signal.

## Get vector collection information

```http
GET /api/v1/nlp/index/info/{project_id}
```

The route returns the vector database collection metadata for the project:

```json
{
  "signal": "vectordb_collection_retrieved",
  "collection_info": {}
}
```

The exact `collection_info` structure is provider-dependent.

## Search indexed context

The primary search endpoint is:

```http
POST /api/v1/nlp/index/search/{project_id}
Content-Type: application/json
```

Request body:

| Field | Type | Default | Constraints |
|---|---:|---:|---|
| `text` | string | required | Must be non-empty after trimming. |
| `limit` | integer | `5` | Must be between `1` and `100`. |

Example:

```bash
curl --fail-with-body --request POST \
  'http://localhost:5000/api/v1/nlp/index/search/demo-project' \
  --header 'Content-Type: application/json' \
  --data '{
    "text": "What is the main topic of the document?",
    "limit": 5
  }'
```

Success response shape:

```json
{
  "signal": "vectordb_search_success",
  "results": [
    {
      "chunk_text": "...",
      "chunk_metadata": {},
      "score": 0.92
    }
  ]
}
```

The exact result fields follow the `RetrievedDocument` model and vector-provider response.

A GET convenience endpoint is also available:

```http
GET /api/v1/nlp/index/search/{project_id}?text=<url-encoded-query>&limit=5
```

The GET route performs the same search operation but currently applies its own default limit of `10`; callers should supply `limit` explicitly when consistent result counts matter.

## Generate a RAG answer

```http
POST /api/v1/nlp/index/answer/{project_id}
Content-Type: application/json
```

The request body uses the same `SearchRequest` schema as semantic search:

```json
{
  "text": "What is the main topic of the document?",
  "limit": 5
}
```

Success response shape:

```json
{
  "signal": "rag_answer_success",
  "answer": "...",
  "full_prompt": "...",
  "chat_history": []
}
```

The `full_prompt` may contain retrieved document content. Treat it as sensitive when documents contain private or regulated information.

## Request validation summary

Pydantic validation occurs before route logic. Invalid JSON fields, missing required search text, invalid chunk parameters, and out-of-range limits produce FastAPI validation responses. Controller-level checks repeat critical chunk and filesystem invariants so direct internal calls cannot bypass the route schema.
