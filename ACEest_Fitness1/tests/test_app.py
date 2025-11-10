"""
Unit tests for the Flask app initialization and basic endpoints.
"""

import pytest
from app.aceest_fitness import create_app


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app = create_app({"TESTING": True, "VERSION": "test-v1"})
    with app.test_client() as client:
        yield client


def test_index_endpoint(client):
    """Check if index route returns correct service info."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "service" in data
    assert data["service"] == "ACEest Fitness API"
    assert data["version"] == "test-v1"


def test_members_list(client):
    """Ensure the members list returns at least 2 entries."""
    resp = client.get("/members")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert "name" in data[0]
    assert "membership" in data[0]
