# Architecture and Data Flow

RAG Project is organized as a small FastAPI application with explicit boundaries between HTTP routes, controllers, persistence models, and provider integrations.

## Component map

```text
Client
  │
  ▼
FastAPI routers (src/routes)
  │
  ├── Request schemas and validation (src/routes/schemes)
  ├── Project, asset, and chunk models (src/models)
  └── Controllers (src/controllers)
        │
        ├── Filesystem storage under src/assets/files
        ├── MongoDB through Motor
        └── NLPController
              ├── Embedding provider
              ├── Qdrant vector database
              ├── TemplateParser
              └── Generation provider
```

## Startup lifecycle

The application is created in [`src/main.py`](https://github.com/Bosaj/RAG_Project/blob/main/src/main.py). During startup it:

1. Loads settings through `get_settings()`.
2. Creates an asynchronous MongoDB client and selects `MONGODB_DATABASE`.
3. Instantiates the LLM and vector database provider factories.
4. Creates the generation client and configures its model.
5. Creates the embedding client and configures its model and vector size.
6. Creates and connects the vector database client.
7. Creates a locale-aware `TemplateParser`.
8. Registers shutdown behavior to close MongoDB and disconnect the vector database.

The startup path intentionally fails early when a selected provider cannot be constructed. The vector database factory raises a descriptive error for unsupported provider names; provider credentials and external service availability are still runtime concerns.

## Ingestion flow

The upload route receives a multipart `UploadFile` at `POST /api/v1/data/upload/{project_id}`. The route ensures that the project exists, validates MIME type and file size through `DataController`, generates a unique project-scoped path, and writes the upload asynchronously in configured chunks.

The filename helper strips path separators and unsafe special characters while preserving a readable name and extension. A random prefix prevents collisions between uploads with the same original name. If writing fails, the partial file is removed before a failure response is returned. After a successful write, an asset record stores the project reference, file identifier, asset type, and file size in MongoDB.

## Processing flow

`POST /api/v1/data/process/{project_id}` accepts a `ProcessRequest`. The route resolves either one requested file or all file assets in the project. `ProcessController` validates the file path against the project storage root, rejects blank or traversal-oriented identifiers, requires regular files, normalizes extensions, and chooses the matching document loader.

The current processing path supports text and PDF files through the existing loader implementations. Extracted content is divided into chunks with the requested `chunk_size` and `overlap_size`. The schema and controller enforce the invariants that `chunk_size` is positive, `overlap_size` is non-negative, and `overlap_size < chunk_size`.

Each chunk becomes a `DataChunk` record with text, metadata, order, project reference, and asset reference. Bulk inserts are performed in batches, and the response reports the number of inserted chunks and processed files.

## Indexing flow

`POST /api/v1/nlp/index/push/{project_id}` reads the project’s chunks from MongoDB in pages. For each page, `NLPController.index_into_vector_db()` embeds the chunk text and inserts the vectors into the project’s vector collection.

When `do_reset` is enabled, reset is requested only for the first page. The helper in [`src/helpers/indexing.py`](https://github.com/Bosaj/RAG_Project/blob/main/src/helpers/indexing.py) keeps reset behavior independent from database imports and prevents later pages from deleting vectors inserted by earlier pages.

Vector identifiers are assigned across pages using a running offset, so a multi-page project receives stable, non-overlapping IDs during one indexing operation.

## Search flow

The search endpoints create or retrieve the project, construct an `NLPController` with the configured embedding and vector database clients, and call `search_vector_db_collection()` with the query text and limit. The embedding client converts the query into a vector, and the vector database returns the most relevant project-scoped records.

The API returns a success signal and serialized search results. An empty or failed result is returned as a `400` response with the vector-search error signal.

## Answer-generation flow

The answer endpoint reuses the search path to retrieve relevant context. `NLPController.answer_rag_question()` then:

1. Builds the query embedding and retrieves relevant documents.
2. Converts retrieved documents into the context representation expected by the prompt template.
3. Loads the localized RAG template through `TemplateParser`.
4. Substitutes context and query values into the full prompt.
5. Sends the prompt to the configured generation client.
6. Returns the answer, full prompt, and chat-history structure.

The full prompt is included in the current API response to support inspection and debugging. Deployments handling sensitive document content should treat that field and application logs as confidential.

## Persistence boundaries

MongoDB stores structured application state:

| Data | Collection role |
|---|---|
| Projects | Identifies the logical project and its storage scope. |
| Assets | Records uploaded files, names, types, sizes, and project ownership. |
| Chunks | Stores processed text, metadata, order, project ownership, and asset ownership. |

The filesystem stores uploaded source files under the application’s assets/files root. Qdrant stores vector representations in project-specific collections derived by the NLP controller.

## Health and readiness semantics

`GET /api/v1/health` returns a lightweight liveness response from the FastAPI process. It is not a full readiness check. MongoDB, Qdrant, and model providers are initialized separately during startup and may fail independently of the route’s simple response.
