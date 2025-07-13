"""
Test module for the main FastAPI application.

This module contains tests for all endpoints defined in src.main.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

# Create a test client for the FastAPI app
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint."""

    def test_root_endpoint_success(self) -> None:
        """Test that the root endpoint returns expected response."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World"
        assert data["status"] == "OK"

    def test_root_endpoint_response_structure(self) -> None:
        """Test that the root endpoint response has correct structure."""
        response = client.get("/")
        data = response.json()

        # Verify all expected keys are present
        expected_keys = {"message", "status"}
        assert set(data.keys()) == expected_keys

        # Verify data types
        assert isinstance(data["message"], str)
        assert isinstance(data["status"], str)


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""

    def test_health_check_success(self) -> None:
        """Test that the health endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "python-template"

    def test_health_check_response_structure(self) -> None:
        """Test that the health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()

        # Verify all expected keys are present
        expected_keys = {"status", "service"}
        assert set(data.keys()) == expected_keys

        # Verify data types
        assert isinstance(data["status"], str)
        assert isinstance(data["service"], str)


class TestAPIStatusEndpoint:
    """Test cases for the API status endpoint."""

    def test_api_status_success(self) -> None:
        """Test that the API status endpoint returns expected response."""
        response = client.get("/api/v1/status")

        assert response.status_code == 200
        data = response.json()
        assert data["api_version"] == "v1"
        assert data["status"] == "running"
        assert data["message"] == "API is operational"

    def test_api_status_response_structure(self) -> None:
        """Test that the API status endpoint response has correct structure."""
        response = client.get("/api/v1/status")
        data = response.json()

        # Verify all expected keys are present
        expected_keys = {"api_version", "status", "message"}
        assert set(data.keys()) == expected_keys

        # Verify data types
        assert isinstance(data["api_version"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["message"], str)


class TestApplicationConfiguration:
    """Test cases for application configuration and metadata."""

    def test_app_metadata(self) -> None:
        """Test that the FastAPI app has correct metadata."""
        assert app.title == "Python Template API"
        assert app.description == "A FastAPI application template"
        assert app.version == "0.1.0"

    def test_cors_middleware_configured(self) -> None:
        """Test that CORS middleware is properly configured."""
        # Check that middleware is added to the app

        # Check if any middleware is CORSMiddleware
        has_cors_middleware = any(
            str(middleware.cls).find("CORSMiddleware") != -1
            for middleware in app.user_middleware
        )
        assert has_cors_middleware, "CORS middleware not found in app middleware stack"


class TestErrorHandling:
    """Test cases for error handling and edge cases."""

    def test_nonexistent_endpoint_returns_404(self) -> None:
        """Test that accessing a non-existent endpoint returns 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_wrong_method_returns_405(self) -> None:
        """Test that using wrong HTTP method returns 405."""
        # Try POST on GET-only endpoints
        response = client.post("/")
        assert response.status_code == 405

        response = client.post("/health")
        assert response.status_code == 405

        response = client.post("/api/v1/status")
        assert response.status_code == 405


class TestResponseHeaders:
    """Test cases for response headers and content type."""

    def test_content_type_json(self) -> None:
        """Test that all endpoints return JSON content type."""
        endpoints = ["/", "/health", "/api/v1/status"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.headers["content-type"] == "application/json"

    def test_response_times(self) -> None:
        """Test that endpoints respond within reasonable time."""
        import time

        endpoints = ["/", "/health", "/api/v1/status"]

        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()

            # Response should be fast (under 1 second for these simple endpoints)
            assert (end_time - start_time) < 1.0
            assert response.status_code == 200


# Fixtures for more complex testing scenarios
@pytest.fixture
def sample_test_data() -> dict[str, dict[str, str]]:
    """Fixture providing sample test data."""
    return {
        "expected_root_response": {"message": "Hello World", "status": "OK"},
        "expected_health_response": {"status": "healthy", "service": "python-template"},
        "expected_api_status_response": {
            "api_version": "v1",
            "status": "running",
            "message": "API is operational",
        },
    }


class TestWithFixtures:
    """Test cases using pytest fixtures."""

    def test_endpoints_with_fixture_data(
        self, sample_test_data: dict[str, dict[str, str]]
    ) -> None:
        """Test endpoints using fixture data for validation."""
        # Test root endpoint
        response = client.get("/")
        assert response.json() == sample_test_data["expected_root_response"]

        # Test health endpoint
        response = client.get("/health")
        assert response.json() == sample_test_data["expected_health_response"]

        # Test API status endpoint
        response = client.get("/api/v1/status")
        assert response.json() == sample_test_data["expected_api_status_response"]


# Integration test example
class TestIntegration:
    """Integration tests for the complete application flow."""

    def test_full_api_workflow(self) -> None:
        """Test a complete workflow using multiple endpoints."""
        # 1. Check that the API is healthy
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"

        # 2. Check API status
        status_response = client.get("/api/v1/status")
        assert status_response.status_code == 200
        assert status_response.json()["status"] == "running"

        # 3. Access root endpoint
        root_response = client.get("/")
        assert root_response.status_code == 200
        assert root_response.json()["status"] == "OK"
