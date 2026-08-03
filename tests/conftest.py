"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from app.main import app, reset_store
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> TestClient:
    reset_store()
    with TestClient(app) as test_client:
        yield test_client
    reset_store()
