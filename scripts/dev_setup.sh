#!/usr/bin/env bash
set -e

echo "=== Setting up RAG Project Development Environment ==="
cd src
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pydantic-settings
if [ ! -f .env ]; then
    cp .env.exemple .env
    echo "Created src/.env from template."
fi
echo "=== Environment Ready! ==="
