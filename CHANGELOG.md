# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog covers changes made in this fork ([Bosaj/RAG_Project](https://github.com/Bosaj/RAG_Project))
on top of the upstream base ([Abdelilah04116/RAG_Project](https://github.com/Abdelilah04116/RAG_Project)).
For the original boilerplate history, see the upstream repository.

## [Unreleased]

### Added
- LanceDB vector-store provider as a pluggable alternative to Qdrant.
- French RAG prompt templates (`src/stores/llm/templates/locales/fr`).
- Sample ENIAD datasets (`data/eniadproject/`) for local, offline pipeline testing.
- `pyproject.toml`, `Makefile`, a `Dockerfile`, and a Qdrant service in Docker Compose.
- Test coverage for the new prompt templates.
- Project documentation under `docs/` (architecture, API reference, deployment).

### Changed
- Modernized the FastAPI app to use a `lifespan` context manager and added CORS middleware.
- Fixed Mermaid diagram rendering and code fences in `README.md`.
- Fixed code fences and path literals in `CONTRIBUTING.md`, `SECURITY.md`, and the PR template.

## [1.0.0] - 2026-08-21

Production-ready release of the RAG engine.

### Added
- FastAPI REST engine with Pydantic v2 settings and asynchronous request handling.
- Qdrant vector database integration with per-project collection isolation.
- Multi-LLM provider support: OpenAI, Google Gemini, Cohere, and Ollama (local LLM).
- Multilingual RAG prompt templates for English and Arabic.
- Liveness endpoint (`GET /api/v1/health`) for deployment probes.
- Request-schema validation for upload, processing, and search/answer endpoints.
- GitHub Actions CI matrix running pytest across Python 3.10, 3.11, and 3.12.
- Code of Conduct, expanded Contributing guidelines, PR template, issue templates, and a Security Policy.

### Changed
- Migrated `Settings` from Pydantic v1-style config to Pydantic v2 `SettingsConfigDict`, and switched path handling to `os.path.realpath`.

### Security
- Canonical path resolution and path-traversal protection for uploaded and processed documents.
- Filename sanitization on upload.
- Validation of processing chunk parameters (chunk size / overlap) and vector-provider names.
- Cleanup of failed uploads and preservation of already-indexed pages on reset.

### Fixed
- Handling of unknown upload sizes during file streaming.

[Unreleased]: https://github.com/Bosaj/RAG_Project/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Bosaj/RAG_Project/releases/tag/v1.0.0
