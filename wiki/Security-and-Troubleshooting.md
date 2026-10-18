# Security and Troubleshooting

RAG Project handles uploaded documents, database credentials, model-provider credentials, and generated prompts. Treat the deployment as a data-processing service and apply least privilege to every external dependency.

## Security controls in the current implementation

| Control | Behavior |
|---|---|
| Project path containment | Project paths are resolved under the configured storage root and rejected when they escape it. |
| File path containment | Processing resolves file IDs within the project directory and rejects traversal attempts. |
| Blank identifier rejection | Blank project IDs and file IDs are rejected instead of being interpreted as the storage root. |
| Regular-file requirement | Directories and non-file paths are not sent to document loaders. |
| Filename sanitization | Uploaded names are normalized to remove path separators and unsafe special characters while retaining a readable extension. |
| Upload validation | MIME type and known file size are checked against configuration. |
| Partial-file cleanup | A failed asynchronous write removes the incomplete file. |
| Schema validation | Chunking, reset flags, search text, and search limits are validated at the HTTP boundary. |
| Lazy optional imports | Heavy ML and vector-provider modules are imported when needed, keeping lightweight routes and tests independent of optional packages. |

These controls reduce common path traversal, malformed-request, and partial-write risks. They do not replace authentication, authorization, encryption, rate limiting, request-size enforcement at the reverse proxy, or provider-specific security controls.

## Secret handling

Keep all credentials in an untracked environment file or a deployment secret manager. Never commit:

- MongoDB usernames, passwords, or connection strings.
- OpenAI, Cohere, Gemini, or other provider API keys.
- Production `.env` files.
- Private uploaded documents, generated prompts, or database dumps.

If a secret is exposed, revoke it immediately, rotate the replacement, inspect logs and repository history, and notify the repository owner through the private process described in [`SECURITY.md`](https://github.com/Bosaj/RAG_Project/blob/main/SECURITY.md).

## Sensitive response fields

The answer endpoint currently returns `full_prompt`, which can include retrieved document text. Do not expose this endpoint publicly without considering whether the prompt or retrieved context contains confidential information. Application logs should be configured so request bodies, provider responses, and credentials are not recorded unintentionally.

## Startup troubleshooting

### Settings validation errors

Confirm that the server is running from `src`, that `src/.env` exists, and that required fields such as `MONGODB_URL`, `MONGODB_DATABASE`, `GENERATION_BACKEND`, `EMBEDDING_BACKEND`, and `VECTOR_DB_BACKEND` are populated.

### MongoDB connection errors

Check that the Compose service is running:

```bash
docker compose --env-file docker/.env -f docker/docker.compose.yml ps
```

Confirm that the host port, credentials, and authentication source in `MONGODB_URL` match the Compose configuration. A healthy container does not guarantee that the application URL is correct.

### Unsupported provider errors

The provider factories raise a descriptive `ValueError` when a backend name is not implemented. Compare the configured name with the provider enums and factory branches. Installing a package does not add support automatically; a provider class and factory integration are required.

### Model authentication or availability errors

Confirm the selected provider’s API key, base URL, model identifier, embedding dimension, and local service status. For Ollama, verify that the service is running and that the configured model has been pulled.

### Upload rejection

Check the file’s MIME type and size against `FILE_ALLOWED_TYPES` and `FILE_MAX_SIZE`. Confirm that the multipart field is named `file`. An unknown streaming size can be accepted, but a known file larger than the configured limit is rejected.

### Processing failure

Confirm that the `file_id` belongs to the specified project, that the stored file still exists, and that the extension is supported. Check that `chunk_size > 0` and `0 <= overlap_size < chunk_size`.

### Search returns no results

Verify the complete lifecycle: upload succeeded, processing inserted chunks, indexing inserted vectors, and the search uses the same `project_id`. Inspect `/api/v1/nlp/index/{project_id}` collection information and provider logs.

### Indexing a large project behaves unexpectedly

Use `do_reset: 1` only when a replacement index is intended. The current implementation resets only the first page, while later pages append. If a previous indexing run partially completed, inspect collection information before deciding whether to reset.

## Production hardening checklist

| Area | Recommendation |
|---|---|
| Network | Put the service behind TLS and a reverse proxy with request-size and timeout limits. |
| Access control | Add authentication and project-level authorization before exposing document routes. |
| Secrets | Use a secret manager and rotate provider/database credentials. |
| Data | Encrypt MongoDB, vector storage, backups, and uploaded files according to the deployment’s sensitivity. |
| Observability | Monitor startup failures, upload failures, indexing failures, provider latency, and storage capacity without logging secrets or document contents. |
| Recovery | Back up MongoDB, filesystem assets, and vector data consistently; document how to rebuild vectors from chunks. |
