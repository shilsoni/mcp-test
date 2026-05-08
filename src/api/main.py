"""
Test API - A simple FastAPI application.

This module provides a basic REST API with health check and sample endpoints.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="MCP Test API",
    description="A simple test API for the MCP Test project",
    version="1.0.0"
)


class Item(BaseModel):
    """Model for an item."""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str


# In-memory storage for demo purposes
items_db: dict[int, Item] = {}
item_counter = 0


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to MCP Test API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.get("/items", tags=["Items"])
async def list_items():
    """List all items."""
    return {"items": list(items_db.values()), "count": len(items_db)}


@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", tags=["Items"])
async def create_item(item: Item):
    """Create a new item."""
    global item_counter
    item_counter += 1
    item.id = item_counter
    items_db[item_counter] = item
    return {"message": "Item created", "item": item}


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = items_db.pop(item_id)
    return {"message": "Item deleted", "item": deleted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
