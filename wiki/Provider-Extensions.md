# Provider Extensions

Provider integrations are selected through factories so the routes and NLP controller can work with a common interface. The current implementation separates language-model providers from vector database providers.

## LLM providers

`LLMProviderFactory` creates generation or embedding clients from the configured backend name. The repository contains provider implementations for OpenAI, Cohere, Gemini, Local embeddings, and Ollama. Provider classes implement the methods expected by the controller, including model configuration, embedding, generation, and provider-specific role handling where applicable.

The LLM factory currently supports these paths:

| Provider path | Typical use |
|---|---|
| `OPENAI` | OpenAI-compatible generation or embedding integration. |
| `COHERE` | Cohere generation or embedding integration. |
| `GEMINI` | Gemini generation or embedding integration. |
| `LOCAL` | Local embedding provider. |
| `OLLAMA` | Local Ollama-backed generation path. |

Before selecting a backend, inspect its provider class to confirm whether it implements generation, embeddings, or both. A backend’s name in `.env` does not itself guarantee that the selected model and provider support the requested operation.

## Vector database providers

`VectorDBProviderFactory` currently supports `QDRANT`. The factory lazily imports the Qdrant implementation, derives a storage path through `BaseController`, and passes the configured distance method. Unsupported names raise:

```text
ValueError: Unsupported vector database provider: '<name>'
```

This makes configuration errors visible at startup rather than allowing a later `NoneType` failure.

## Adding a new LLM provider

A new LLM provider should follow the existing interface and be integrated deliberately:

1. Add a provider class under `src/stores/llm/providers/`.
2. Implement the generation or embedding interface required by the controller.
3. Add or update an enum value if the provider name is represented by an enum.
4. Add the factory branch in `LLMProviderFactory.create()`.
5. Document credentials, model identifiers, and capability limitations in [[Configuration Reference]].
6. Add unit tests for provider selection and configuration behavior without making network calls.
7. Update the README, CI dependency list, and this page.

Provider tests should use mocks or minimal configuration objects. Unit tests must not depend on a live provider account or external API.

## Adding a new vector provider

A new vector provider should implement the methods declared by [`VectorDBInterface`](https://github.com/Bosaj/RAG_Project/blob/main/src/stores/vectordb/VectorDBInterface.py), including connection lifecycle, collection management, insertion, and search.

Recommended sequence:

1. Add the provider implementation under `src/stores/vectordb/providers/`.
2. Add a provider enum value in `VectorDBEnums.py`.
3. Add a lazy factory branch in `VectorDBProviderFactory.create()`.
4. Add configuration variables and document their types and defaults.
5. Confirm that collection naming and project isolation remain compatible with `NLPController`.
6. Add unit tests for unsupported-provider errors and provider selection without importing optional SDKs unnecessarily.
7. Add an integration test separately if the provider requires a live service.

## Dependency boundaries

Optional provider dependencies should be imported lazily whenever a lightweight route or unit test does not need them. This keeps schema, filesystem, and controller validation tests runnable in minimal CI environments and makes failures point to the selected integration rather than an unrelated import.

When adding a dependency, update `src/requirements.txt`, the CI installation step, the environment template if configuration is required, and the operational documentation.

## Provider safety checklist

| Question | Expected answer |
|---|---|
| Does the provider implement the required interface? | Yes, with clear behavior for connect, configure, embed/generate, search, and disconnect. |
| Are unsupported names rejected? | Yes, with a descriptive exception. |
| Are credentials kept out of code and tests? | Yes, through environment settings or a secret manager. |
| Can unit tests run without a live service? | Yes, through mocks and isolated factory checks. |
| Is project isolation preserved? | Yes, every collection and query must remain scoped to the project. |
| Are failure modes documented? | Yes, including authentication, connectivity, model, dimension, and timeout failures. |
