"""Integration tests — exercise multi-step API flows end to end."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_list_get_flow(client: TestClient) -> None:
    """Create two items, list them, then fetch one by id."""
    first = client.post("/api/items", json={"name": "alpha", "quantity": 1})
    second = client.post("/api/items", json={"name": "beta", "quantity": 5})
    assert first.status_code == 201
    assert second.status_code == 201

    listed = client.get("/api/items")
    assert listed.status_code == 200
    names = {item["name"] for item in listed.json()}
    assert names == {"alpha", "beta"}

    item_id = first.json()["id"]
    fetched = client.get(f"/api/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json() == {"id": item_id, "name": "alpha", "quantity": 1}


def test_health_matches_version_environment(client: TestClient) -> None:
    health = client.get("/health").json()
    version = client.get("/version").json()
    assert health["environment"] == version["environment"]
    assert health["version"] == version["version"]
