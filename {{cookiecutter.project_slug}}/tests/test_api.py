"""Unit tests for example API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint() -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_list_examples() -> None:
    """Test listing examples."""
    response = client.get("/api/v1/example/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_example() -> None:
    """Test creating an example."""
    example_data = {
        "name": "Test Example",
        "description": "Test description",
    }
    response = client.post("/api/v1/example/", json=example_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == example_data["name"]


def test_trigger_task() -> None:
    """Test triggering a Celery task."""
    response = client.post("/api/v1/example/task?message=test")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data

