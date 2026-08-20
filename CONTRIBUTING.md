# Contributing

Thank you for helping improve RAG Project. Contributions should solve a real problem, improve reliability, or make the project easier to use.

## Before you start

Read the README and confirm that the change fits the project’s document-processing and retrieval workflow. For security issues, follow [`SECURITY.md`](SECURITY.md) instead of opening a public issue.

## Local setup

The application runs from `src` because its configuration loader reads `.env` from the current working directory.

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.exemple .env
```

## Making a change

Create a focused branch from `main`. Keep production changes small and explain the behavior being changed. Do not commit `.env` files, API keys, database credentials, private documents, generated caches, or large unrelated files.

Run the project’s checks before opening a pull request:

```bash
python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover --start-directory tests --pattern 'test_*.py' --verbose
```

If the change affects an endpoint or request schema, add or update a regression test. If the change affects setup or API behavior, update the README as part of the same pull request.

## Pull requests

Use a descriptive title and explain the problem, the approach, and the verification performed. Keep one logical change per pull request. Maintainers may request revisions before merging.
