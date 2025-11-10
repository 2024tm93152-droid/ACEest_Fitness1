"""
Detailed route tests for ACEest Fitness API.
Focus on POST /members, GET /members/<id>, and error handling.
"""

import pytest
from app.aceest_fitness1 import create_app


@pytest.fixture
def client():
    """Reusable test client."""
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_add_member_success(client):
    """POST /members should add a valid member and return 201."""
    payload = {"name": "Charlie", "membership": "premium"}
    resp = client.post("/members", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Charlie"
    assert data["membership"] == "premium"
    assert "id" in data


def test_add_member_missing_fields(client):
    """POST /members should fail when required fields are missing."""
    resp = client.post("/members", json={"name": "NoMembership"})
    assert resp.status_code == 400
    assert b"name and membership required" in resp.data


def test_get_existing_member(client):
    """GET /members/<id> should return correct member."""
    resp = client.get("/members/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1
    assert "name" in data
    assert "membership" in data


def test_get_nonexistent_member(client):
    """GET /members/<id> with invalid ID should return 404."""
    resp = client.get("/members/9999")
    assert resp.status_code == 404
    assert b"Member not found" in resp.data


def test_add_member_invalid_json(client):
    """POST /members without JSON body should return 400."""
    resp = client.post("/members", data="not-json", content_type="text/plain")
    assert resp.status_code == 400
    assert b"JSON required" in resp.data
