"""Minimal FastAPI service — the artifact the CI/CD pipeline builds, tests, and deploys."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import Settings, get_settings

settings: Settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Demo API used to practice a modern CI/CD pipeline.",
)

# In-memory store — enough for unit/integration tests without a database.
_ITEMS: dict[int, dict] = {}
_NEXT_ID = 1


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    quantity: int = Field(default=1, ge=1, le=1000)


class Item(ItemCreate):
    id: int


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        version=settings.version,
    )


@app.get("/version")
def version() -> dict[str, str]:
    return {
        "app": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
    }


@app.get("/api/items", response_model=list[Item])
def list_items() -> list[Item]:
    return [Item(**item) for item in _ITEMS.values()]


@app.post("/api/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate) -> Item:
    global _NEXT_ID
    item = {"id": _NEXT_ID, "name": payload.name, "quantity": payload.quantity}
    _ITEMS[_NEXT_ID] = item
    _NEXT_ID += 1
    return Item(**item)


@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = _ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**item)


def reset_store() -> None:
    """Test helper — clears the in-memory store between tests."""
    global _NEXT_ID
    _ITEMS.clear()
    _NEXT_ID = 1
