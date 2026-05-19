.PHONY: help install test run lint format clean docker-build docker-up docker-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	python -m venv venv
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt

test: ## Run tests
	source venv/bin/activate && pytest

run: ## Run the API server
	source venv/bin/activate && uvicorn thermaguard.api.main:app --reload --host 0.0.0.0 --port 8000

worker: ## Run Celery worker
	source venv/bin/activate && celery -A thermaguard.tasks.celery_app worker --loglevel=info

beat: ## Run Celery beat scheduler
	source venv/bin/activate && celery -A thermaguard.tasks.celery_app beat --loglevel=info

lint: ## Run linting
	source venv/bin/activate && ruff check thermaguard/
	source venv/bin/activate && mypy thermaguard/

format: ## Format code
	source venv/bin/activate && black thermaguard/
	source venv/bin/activate && ruff check --fix thermaguard/

clean: ## Clean up generated files
	rm -rf venv/
	rm -rf logs/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf thermaguard/__pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

docker-build: ## Build Docker image
	docker build -t thermaguard-ai .

docker-up: ## Start Docker Compose services
	docker-compose up -d

docker-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker Compose logs
	docker-compose logs -f
