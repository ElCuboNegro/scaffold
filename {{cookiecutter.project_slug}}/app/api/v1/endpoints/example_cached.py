{% if cookiecutter.use_redis == "yes" -%}
"""Example endpoint with Redis caching."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import delete_cache, get_cache, get_db, set_cache
from app.crud import example as crud
from app.schemas.example import ExampleResponse

router = APIRouter()


@router.get("/{example_id}/cached", response_model=ExampleResponse)
async def get_example_cached(
    example_id: int,
    db: Session = Depends(get_db),
) -> ExampleResponse:
    """
    Get a specific example by ID with Redis caching.

    This demonstrates caching pattern:
    1. Check cache first
    2. If not found, query database
    3. Store result in cache
    4. Return result

    Args:
        example_id: ID of the example to retrieve

    Returns:
        Example with the specified ID (cached or from DB)

    Raises:
        HTTPException: 404 if example not found
    """
    # Check cache first
    cache_key = f"example:{example_id}"
    cached_example = get_cache(cache_key)
    
    if cached_example:
        # Return cached result
        return ExampleResponse(**cached_example)
    
    # Cache miss - query database
    db_example = crud.get_example(db=db, example_id=example_id)
    if not db_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )
    
    # Convert to dict for caching
    example_dict = {
        "id": db_example.id,
        "name": db_example.name,
        "description": db_example.description,
    }
    
    # Store in cache (1 hour TTL)
    set_cache(cache_key, example_dict, ttl=3600)
    
    return ExampleResponse(**example_dict)


def invalidate_example_cache(example_id: int) -> None:
    """
    Invalidate cache for a specific example.

    Call this after UPDATE or DELETE operations.

    Args:
        example_id: ID of the example to invalidate
    """
    cache_key = f"example:{example_id}"
    delete_cache(cache_key)
{% else -%}
"""Cached endpoint placeholder - Redis not enabled."""

# Cached endpoints disabled in this configuration
# To enable, regenerate with use_redis=yes
{% endif -%}
