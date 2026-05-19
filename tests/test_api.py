"""
API endpoint tests.
"""

import pytest
from fastapi.testclient import TestClient
from thermaguard.api.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_ingest_reading():
    """Test sensor reading ingestion."""
    response = client.post(
        "/api/v1/ingest",
        json={
            "chamber_id": "test_chamber",
            "timestamp": "2024-01-15T10:30:00Z",
            "temperature": -15.5,
            "sensor_id": "sensor_001"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"


def test_ingest_batch():
    """Test batch sensor reading ingestion."""
    response = client.post(
        "/api/v1/ingest/batch",
        json={
            "readings": [
                {
                    "chamber_id": "test_chamber",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "temperature": -15.5,
                    "sensor_id": "sensor_001"
                },
                {
                    "chamber_id": "test_chamber",
                    "timestamp": "2024-01-15T10:31:00Z",
                    "temperature": -15.3,
                    "sensor_id": "sensor_001"
                }
            ]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 2
