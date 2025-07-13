.PHONY: help install test test-cov format format-check lint autofix check-all ci security update build clean dev docker-build docker-run docker-stop docker-logs
CODE_DIRS = src/ tests/

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and setup hooks
	@set -e; \
	echo "Installing dependencies..."; \
	uv sync --group dev; \
	echo "Setting up pre-commit hooks..."; \
	uv run pre-commit install; \
	echo "✅ Installation complete!"

test: ## Run tests with coverage (default)
	@set -e; \
	echo "Running tests with coverage..."; \
	uv run pytest tests/ -v -n auto --cov=src --cov-report=term-missing --cov-report=html

test-simple: ## Run tests without coverage (faster)
	@set -e; \
	echo "Running tests..."; \
	uv run pytest tests/ -v -n auto

format: ## Format code using Ruff formatter
	@set -e; \
	echo "Formatting code..."; \
	uv run ruff format $(CODE_DIRS); \
	echo "✅ Code formatted!"

format-check: ## Check if code is formatted correctly (for CI)
	@set -e; \
	echo "Checking code formatting..."; \
	uv run ruff format --check $(CODE_DIRS)

lint: ## Check for linting issues using Ruff (no fixes)
	@set -e; \
	echo "Linting code..."; \
	uv run ruff check $(CODE_DIRS)

autofix: ## Fix linting issues and format code
	@set -e; \
	echo "Fixing linting issues and formatting code..."; \
	uv run ruff check --fix $(CODE_DIRS); \
	uv run ruff format $(CODE_DIRS); \
	echo "✅ Code auto-fixed and formatted!"

security: ## Run security checks with bandit
	@set -e; \
	echo "Running security checks..."; \
	uv run bandit -r src/ -f json -o bandit-report.json || uv run bandit -r src/; \
	echo "✅ Security check complete!"

update: ## Update dependencies to latest versions
	@set -e; \
	echo "Updating dependencies..."; \
	uv sync --upgrade; \
	echo "✅ Dependencies updated!"

build: ## Build the package
	@set -e; \
	echo "Building package..."; \
	uv build; \
	echo "✅ Package built successfully!"

ci: format-check lint security test ## Run all CI checks (no fixes, just validation)
	@echo "✅ All CI checks passed!"

check-all: lint format-check test security ## Run all checks (comprehensive)
	@echo "✅ All checks complete!"

dev: ## Start development mode with file watching
	@echo "Starting development mode..."
	@echo "💡 Tip: Use 'make autofix' in another terminal for quick fixes"
	uv run pytest tests/ -n auto --cov=src -f

clean: ## Clean up generated files
	@set -e; \
	echo "Cleaning up generated files..."; \
	rm -rf .pytest_cache/ htmlcov/ .coverage .mypy_cache/ __pycache__/ dist/ build/ *.egg-info/; \
	find . -type d -name "__pycache__" -delete; \
	find . -type f -name "*.pyc" -delete; \
	find . -type f -name "bandit-report.json" -delete; \
	echo "Cleaning Jupyter notebooks..."; \
	find . -name "*.ipynb" -exec nbstripout {} \; 2>/dev/null || true; \
	echo "✅ Cleanup complete!"

# Docker commands
docker-build: ## Build Docker image
	@set -e; \
	echo "Building Docker image..."; \
	docker build -t python-template:latest .; \
	echo "✅ Docker image built!"

docker-run: ## Run the application in Docker
	@set -e; \
	echo "Starting application with Docker Compose..."; \
	docker-compose up -d; \
	echo "✅ Application started at http://localhost:8000"

docker-stop: ## Stop Docker containers
	@set -e; \
	echo "Stopping Docker containers..."; \
	docker-compose down; \
	echo "✅ Docker containers stopped!"

docker-logs: ## View Docker container logs
	@docker-compose logs -f app
