.PHONY: help install run test lint format docker-up docker-down clean

help:
	@echo "RAG Project Development Commands:"
	@echo "  make install     - Install application and dev dependencies"
	@echo "  make run         - Start the FastAPI backend server with auto-reload"
	@echo "  make test        - Run the full test suite with pytest"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black and isort"
	@echo "  make docker-up   - Start MongoDB and services with Docker Compose"
	@echo "  make docker-down - Stop all Docker Compose services"
	@echo "  make clean       - Remove cache and build artifacts"

install:
	python -m pip install --upgrade pip
	python -m pip install -r src/requirements.txt
	python -m pip install pytest pydantic-settings

run:
	cd src && uvicorn main:app --reload --host 0.0.0.0 --port 5000

test:
	PYTHONPATH=src pytest -v

lint:
	python -m compileall -q src tests

docker-up:
	docker compose --env-file docker/.env -f docker/docker.compose.yml up -d

docker-down:
	docker compose --env-file docker/.env -f docker/docker.compose.yml down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
