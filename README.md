# Python Template

A modern Python FastAPI application template with comprehensive development tooling and Docker deployment support.

## Features

- **FastAPI** web framework with modern Python 3.11+
- **UV** for fast dependency management
- **Ruff** for code formatting and linting
- **MyPy** for static type checking
- **Pytest** with coverage reporting
- **Pre-commit hooks** for automated code quality
- **DevContainer** support for consistent development
- **Docker** deployment ready

## Quick Start

### Development Setup

1. **Using DevContainer (Recommended)**:
   - Open in VS Code with the Dev Containers extension
   - The container will automatically set up the environment

2. **Local Development**:
   ```bash
   # Install dependencies
   make install

   # Run tests
   make test

   # Start development server
   make dev
   ```

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   make docker-build
   make docker-run
   ```

2. **Manual Docker commands**:
   ```bash
   # Build image
   docker build -t python-template:latest .

   # Run container
   docker run -p 8000:8000 python-template:latest
   ```

3. **View logs**:
   ```bash
   make docker-logs
   ```

4. **Stop containers**:
   ```bash
   make docker-stop
   ```

## Available Commands

Run `make help` to see all available commands:

- `make install` - Install dependencies and setup hooks
- `make test` - Run tests with coverage
- `make format` - Format code using Ruff
- `make lint` - Check for linting issues
- `make autofix` - Fix linting issues and format code
- `make security` - Run security checks
- `make docker-build` - Build Docker image
- `make docker-run` - Run with Docker Compose
- `make docker-stop` - Stop Docker containers

## API Endpoints

Once running, the API will be available at:

- **Root**: `http://localhost:8000/` - Hello World
- **Health Check**: `http://localhost:8000/health` - Health status
- **API Status**: `http://localhost:8000/api/v1/status` - API status
- **Interactive Docs**: `http://localhost:8000/docs` - Swagger UI
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API docs

## Project Structure

```
├── src/                    # Application source code
│   └── main.py            # FastAPI application entry point
├── tests/                 # Test files
├── .devcontainer/         # DevContainer configuration
├── Dockerfile             # Production Docker image
├── docker-compose.yml     # Docker Compose configuration
├── pyproject.toml         # Project configuration and dependencies
├── Makefile              # Development commands
└── .pre-commit-config.yaml # Pre-commit hooks configuration
```

## Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework
- **SQLAlchemy**: Database ORM
- **Pydantic Settings**: Configuration management
- **Structlog**: Structured logging
- **python-jose**: JWT authentication
- **passlib**: Password hashing

### Development Dependencies
- **Pytest**: Testing framework
- **Ruff**: Linting and formatting
- **MyPy**: Static type checking
- **Bandit**: Security scanning
- **Pre-commit**: Git hooks
