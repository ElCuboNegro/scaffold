"""Example endpoint demonstrating API structure."""

from fastapi import APIRouter{% if cookiecutter.use_postgresql == "yes" %}, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import example as crud
from app.models.example import Example{% endif %}
from app.schemas.example import ExampleCreate, ExampleResponse, ExampleUpdate
from app.schemas.pagination import PaginatedResponse
from app.tasks.example import example_task

router = APIRouter()


@router.get("/", response_model={% if cookiecutter.use_postgresql == "yes" %}PaginatedResponse[ExampleResponse]{% else %}list[ExampleResponse]{% endif %})
async def list_examples({% if cookiecutter.use_postgresql == "yes" %}
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    description: str | None = None,{% endif %}
) -> {% if cookiecutter.use_postgresql == "yes" %}PaginatedResponse[ExampleResponse]{% else %}list[ExampleResponse]{% endif %}:
    """
    List all examples with pagination and optional filtering.

    Args:
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        name: Optional filter by name (partial match)
        description: Optional filter by description (partial match)

    Returns:
        Paginated list of examples with metadata
    """
    {% if cookiecutter.use_postgresql == "yes" -%}
    # Build query with optional filters
    query = select(Example)

    if name:
        query = query.where(Example.name.ilike(f"%{name}%"))
    if description:
        query = query.where(Example.description.ilike(f"%{description}%"))

    # Get total count
    count_query = select(func.count()).select_from(Example)
    if name:
        count_query = count_query.where(Example.name.ilike(f"%{name}%"))
    if description:
        count_query = count_query.where(Example.description.ilike(f"%{description}%"))
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    # Calculate pagination metadata
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = (total + limit - 1) // limit if limit > 0 else 1

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=limit,
        pages=pages,
    )
    {% else -%}
    # Fallback for non-database configuration
    return [
        ExampleResponse(id=1, name="Example 1", description="First example"),
        ExampleResponse(id=2, name="Example 2", description="Second example"),
    ]
    {% endif %}


@router.post("/", response_model=ExampleResponse, status_code=201)
async def create_example({% if cookiecutter.use_postgresql == "yes" %}
    *,
    db: AsyncSession = Depends(get_db),
    example_in: ExampleCreate,{% else %}
    example_in: ExampleCreate,{% endif %}
) -> ExampleResponse:
    """
    Create a new example.

    Args:
        example_in: Example data to create

    Returns:
        Created example with generated ID
    """
    {% if cookiecutter.use_postgresql == "yes" -%}
    return await crud.create_example(db=db, example=example_in)
    {% else -%}
    # Fallback for non-database configuration
    return ExampleResponse(
        id=1,
        name=example_in.name,
        description=example_in.description,
    )
    {% endif %}


@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example({% if cookiecutter.use_postgresql == "yes" %}
    example_id: int,
    db: AsyncSession = Depends(get_db),{% else %}
    example_id: int,{% endif %}
) -> ExampleResponse:
    """
    Get a specific example by ID.

    Args:
        example_id: ID of the example to retrieve

    Returns:
        Example with the specified ID

    Raises:
        HTTPException: 404 if example not found
    """
    {% if cookiecutter.use_postgresql == "yes" -%}
    db_example = await crud.get_example(db=db, example_id=example_id)
    if not db_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )
    return db_example
    {% else -%}
    # Fallback for non-database configuration
    return ExampleResponse(
        id=example_id,
        name=f"Example {example_id}",
        description=f"Description for example {example_id}",
    )
    {% endif %}


@router.put("/{example_id}", response_model=ExampleResponse)
async def update_example({% if cookiecutter.use_postgresql == "yes" %}
    example_id: int,
    example_in: ExampleUpdate,
    db: AsyncSession = Depends(get_db),{% else %}
    example_id: int,
    example_in: ExampleUpdate,{% endif %}
) -> ExampleResponse:
    """
    Update an existing example.

    Args:
        example_id: ID of the example to update
        example_in: Updated example data (partial updates supported)

    Returns:
        Updated example

    Raises:
        HTTPException: 404 if example not found
    """
    {% if cookiecutter.use_postgresql == "yes" -%}
    db_example = await crud.update_example(db=db, example_id=example_id, example=example_in)
    if not db_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )
    return db_example
    {% else -%}
    # Fallback for non-database configuration
    return ExampleResponse(
        id=example_id,
        name=example_in.name or f"Example {example_id}",
        description=example_in.description or f"Updated description {example_id}",
    )
    {% endif %}


@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example({% if cookiecutter.use_postgresql == "yes" %}
    example_id: int,
    db: AsyncSession = Depends(get_db),{% else %}
    example_id: int,{% endif %}
) -> None:
    """
    Delete an example.

    Args:
        example_id: ID of the example to delete

    Raises:
        HTTPException: 404 if example not found
    """
    {% if cookiecutter.use_postgresql == "yes" -%}
    success = await crud.delete_example(db=db, example_id=example_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )
    {% else -%}
    # Fallback for non-database configuration
    pass
    {% endif %}


@router.post("/task", response_model=dict[str, str])
async def trigger_example_task(message: str) -> dict[str, str]:
    """
    Trigger an example Celery task.

    This demonstrates async task execution.

    Args:
        message: Message to process in background task

    Returns:
        Task ID and status information
    """
    task = example_task.delay(message)
    return {
        "task_id": task.id,
        "status": "Task queued",
        "message": f"Processing: {message}",
    }
