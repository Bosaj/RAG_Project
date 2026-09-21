# Testing and Contributing

The project favors small, reviewable changes with focused regression tests. The repository’s contribution guide is [`CONTRIBUTING.md`](https://github.com/Bosaj/RAG_Project/blob/main/CONTRIBUTING.md), and the CI workflow is [`python-checks.yml`](https://github.com/Bosaj/RAG_Project/blob/main/.github/workflows/python-checks.yml).

## Local development setup

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The tests are intentionally structured so validation and controller behavior can run without connecting to MongoDB, Qdrant, or external model providers.

## Run the test suite

From the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover \
  --start-directory tests \
  --pattern 'test_*.py' \
  --verbose
```

The suite covers request schemas and health behavior, project path safety, upload validation and filename sanitization, document path and chunking invariants, paginated indexing reset behavior, and unsupported vector-provider errors.

## Compile and whitespace checks

Run the same checks used by the repository workflow:

```bash
python3 -m compileall -q src tests
git diff --check
```

`compileall` catches syntax and bytecode-compilation failures. `git diff --check` catches whitespace errors in the proposed diff.

## Continuous integration

The GitHub Actions workflow runs on pushes and pull requests. It installs the pinned FastAPI/Pydantic dependencies needed by the lightweight tests, compiles source and tests, and runs unittest discovery. Keep CI deterministic: do not require a live MongoDB, Qdrant instance, provider API key, or external model for unit tests.

## Making a focused change

Before changing code, identify the user-visible or operational problem and locate the narrowest layer that owns the behavior. For example, request invariants belong in Pydantic schemas and defensive controller validation, while provider selection belongs in the provider factory.

A focused contribution should:

1. Explain the problem and the intended behavior.
2. Add or update a regression test for the changed behavior.
3. Update the README or wiki when commands, endpoints, configuration, or operational behavior changes.
4. Avoid unrelated refactors, generated artifacts, secrets, and private data.
5. Run the complete local suite, compilation check, and whitespace check.
6. Describe verification results clearly in the pull request.

## Pull-request checklist

| Check | Command or action |
|---|---|
| Scope | Confirm the diff solves one coherent problem. |
| Tests | Run the complete unittest discovery command. |
| Syntax | Run `python3 -m compileall -q src tests`. |
| Diff hygiene | Run `git diff --check`. |
| Documentation | Update README/wiki for changed behavior. |
| Security | Confirm no secrets, credentials, private documents, or generated dumps are included. |
| Compatibility | Check that optional provider dependencies are not imported by tests that do not need them. |
| Review | Explain the behavior change, test evidence, and operational impact. |

## Test organization

| File | Scope |
|---|---|
| `tests/test_request_schemas.py` | Pydantic request validation and the liveness response. |
| `tests/test_project_controller.py` | Project identifier validation and storage-root containment. |
| `tests/test_data_controller.py` | Upload filename normalization, type/size checks, and streaming behavior. |
| `tests/test_process_controller.py` | File-path safety, extension handling, and chunking parameter invariants. |
| `tests/test_nlp_indexing.py` | Reset-on-first-page behavior for paginated vector indexing. |
| `tests/test_provider_factories.py` | Actionable unsupported-vector-provider errors without optional Qdrant imports. |

## Documentation maintenance

When endpoint behavior changes, update the API Reference and the relevant request-schema tests. When storage or security behavior changes, update Data Model and Storage and Security and Troubleshooting. When provider support changes, update Configuration Reference, Provider Extensions, and the provider tests.
