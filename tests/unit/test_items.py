"""Unit tests for the items API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_items_empty(client: TestClient) -> None:
    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client: TestClient) -> None:
    response = client.post("/api/items", json={"name": "widget", "quantity": 3})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "widget"
    assert body["quantity"] == 3


def test_create_item_rejects_empty_name(client: TestClient) -> None:
    response = client.post("/api/items", json={"name": "", "quantity": 1})
    assert response.status_code == 422


def test_get_item(client: TestClient) -> None:
    created = client.post("/api/items", json={"name": "gasket", "quantity": 2}).json()
    response = client.get(f"/api/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "gasket"


def test_get_missing_item(client: TestClient) -> None:
    response = client.get("/api/items/999")
    assert response.status_code == 404


def test_create_item_default_quantity(client: TestClient) -> None:
    response = client.post("/api/items", json={"name": "bolt"})
    assert response.status_code == 201
    assert response.json()["quantity"] == 1
