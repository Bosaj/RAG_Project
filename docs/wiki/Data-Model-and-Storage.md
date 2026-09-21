# Data Model and Storage

RAG Project uses MongoDB for structured application state, the local filesystem for uploaded source files, and Qdrant for vector representations. A project identifier is the boundary that connects these stores.

## Project identity

A project is identified by `project_id`. The project model enforces an alphanumeric project identifier and creates a unique index on that field. Routes use `get_project_or_create_one()` so a first upload or processing request can initialize the project record.

Project identifiers also determine the filesystem scope and vector collection scope. Do not use path separators, blank identifiers, or identifiers that attempt to escape the configured storage root.

## MongoDB collections

### Projects

The project document stores the logical project identifier and MongoDB metadata. A unique index prevents duplicate project identifiers.

### Assets

An asset represents an uploaded file:

| Field | Meaning |
|---|---|
| `asset_project_id` | MongoDB identifier of the owning project. |
| `asset_type` | Asset category; uploaded files use the file asset enum value. |
| `asset_name` | Generated file identifier and stored filename. |
| `asset_size` | Size recorded after a successful filesystem write. |
| `asset_config` | Optional provider or processing metadata. |
| `asset_pushed_at` | Timestamp field available for indexing lifecycle metadata. |

The asset model maintains project-oriented lookup support and a unique compound index over project and asset name.

### Chunks

A processed chunk stores extracted text and its source context:

| Field | Meaning |
|---|---|
| `chunk_text` | Text used for embedding and retrieval. |
| `chunk_metadata` | Loader and document metadata. |
| `chunk_order` | Position of the chunk within the source asset. |
| `chunk_project_id` | Owning project reference. |
| `chunk_asset_id` | Source asset reference. |

Chunk queries are project-scoped. Bulk insertion is performed in batches of 100, and indexing reads project chunks in pages of 50.

## Filesystem layout

The base controller derives storage roots under the application’s `src/assets` directory:

```text
src/
└── assets/
    ├── files/
    │   └── <project-scoped uploaded files>
    └── database/
        └── <vector database provider paths>
```

`ProjectController` constrains project directories to the files storage root. `ProcessController` resolves file IDs against the project directory, rejects traversal outside that root, rejects blank IDs, requires regular files, and normalizes extensions case-insensitively.

Uploaded filenames are sanitized before path construction. The generated filename keeps a readable safe portion and uses a random prefix to reduce collisions. If an input name contains no usable characters, the controller falls back to a safe generated name.

## Vector database scope

The current vector database factory supports Qdrant. The provider receives a database path derived through the shared database storage helper and a configured distance method. The NLP controller derives a collection name from the project, keeping vector search isolated between projects.

Indexing uses a running integer offset when processing pages. This prevents duplicate vector IDs across page boundaries. When reset is requested, only the first page triggers collection reset; later pages append to the same collection.

## Lifecycle and reset behavior

The intended lifecycle is:

```text
Project created
  → Asset metadata created after upload
  → Chunks inserted after processing
  → Vectors inserted after indexing
  → Search and answer operations read the vector collection
```

Processing reset and indexing reset are separate operations. Processing reset deletes MongoDB chunks for a project before rebuilding them. Indexing reset clears or recreates the vector collection only at the first indexing page. Use both resets when replacing a project’s corpus from scratch; omit them when adding new material.

## Operational consistency

The application does not describe a distributed transaction across filesystem, MongoDB, and Qdrant. A successful upload writes the file before creating the asset record; a failed file write removes the partial file. Processing and indexing are separate explicit calls, so operators should treat their responses as lifecycle checkpoints and retry failed stages deliberately.
