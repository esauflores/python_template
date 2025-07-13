"""
Pytest configuration and shared fixtures for the test suite.

This module contains pytest configuration and fixtures that are shared
across multiple test modules.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    """
    Create a test client for the FastAPI application.

    This fixture is session-scoped, meaning it's created once per test session
    and reused across all tests for better performance.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def fresh_client() -> TestClient:
    """
    Create a fresh test client for each test function.

    Use this fixture when you need a clean client instance for each test,
    for example when testing stateful operations.
    """
    return TestClient(app)


@pytest.fixture
def api_endpoints() -> list[str]:
    """Fixture providing a list of all API endpoints for testing."""
    return ["/", "/health", "/api/v1/status"]


@pytest.fixture
def expected_responses() -> dict[str, dict[str, str]]:
    """Fixture providing expected responses for all endpoints."""
    return {
        "/": {"message": "Hello World", "status": "OK"},
        "/health": {"status": "healthy", "service": "python-template"},
        "/api/v1/status": {
            "api_version": "v1",
            "status": "running",
            "message": "API is operational",
        },
    }


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
