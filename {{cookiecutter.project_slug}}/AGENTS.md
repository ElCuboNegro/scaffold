# Developer & Agent Guide

This document provides instructions for extending the application.

## 1. Testing (BDD with Behave)

This project uses **Behavior Driven Development (BDD)** with `behave` for testing.

*   **Feature Files**: Located in `features/`. Define scenarios in Gherkin syntax.
*   **Step Definitions**: Located in `features/steps/`. Implement the Python code for each step.
*   **Running Tests**:
    ```bash
    # Run all tests
    docker compose run --rm api behave

    # Run specific feature
    docker compose run --rm api behave features/my_feature.feature
    ```

**Example Feature (`features/example.feature`):**
```gherkin
Feature: Example Feature
  Scenario: Successful operation
    Given the database is empty
    When I request the example endpoint
    Then I should receive a 200 response
```

## 2. Pydantic Models (Schemas)

Pydantic models are used for request validation and response serialization. They are located in `app/schemas/`.

*   **Create a new file** (e.g., `app/schemas/item.py`) or add to an existing one.
*   **Define Models**:
    *   `ItemBase`: Shared properties.
    *   `ItemCreate`: Properties required for creation.
    *   `ItemUpdate`: Properties for updates (all optional).
    *   `Item`: Properties returned to the client (includes `id`, `created_at`).

**Example:**
```python
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
```

## 3. Relationships & Migrations (SQLAlchemy & Alembic)

Database models are defined using SQLAlchemy in `app/models/`.

*   **Define Model**: Create a class inheriting from `Base` in `app/models/`.
*   **Relationships**: Use `relationship()` to define links between tables.

**Example (`app/models/item.py`):**
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

**Migrations:**
After modifying models, generate and apply migrations:

```bash
# Generate migration
docker compose run --rm api alembic revision --autogenerate -m "Add items table"

# Apply migration
docker compose run --rm api alembic upgrade head
```

## 4. RESTful Endpoints (FastAPI)

API endpoints are located in `app/api/v1/endpoints/`.

1.  **Create Router**: Create a new file (e.g., `app/api/v1/endpoints/items.py`).
2.  **Define Endpoints**: Use `APIRouter` to define `GET`, `POST`, `PUT`, `DELETE` operations.
3.  **Register Router**: Add the router to `app/api/v1/api.py`.

**Example (`app/api/v1/endpoints/items.py`):**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import item as schemas

router = APIRouter()

@router.post("/", response_model=schemas.Item)
async def create_item(
    item: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    # Implementation here
    pass
```
