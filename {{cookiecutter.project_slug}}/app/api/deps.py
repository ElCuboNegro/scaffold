"""API dependency injection."""

{% if cookiecutter.use_postgresql == "yes" -%}
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db as get_db_session

# Re-export for convenience
get_db = get_db_session
{% else -%}
# Database dependencies disabled - PostgreSQL not enabled
{% endif %}

{% if cookiecutter.use_redis == "yes" -%}
import json
from typing import Any

import redis
from app.core.config import settings

# Redis client for caching
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis() -> redis.Redis:
    """Dependency for Redis client."""
    return redis_client


def get_cache(key: str) -> Any | None:
    """
    Get value from cache.
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None


def set_cache(key: str, value: Any, ttl: int = 3600) -> None:
    """
    Set value in cache with TTL.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default: 1 hour)
    """
    redis_client.setex(key, ttl, json.dumps(value))


def delete_cache(pattern: str) -> None:
    """
    Delete cache keys matching pattern.
    
    Args:
        pattern: Redis key pattern (e.g., "example:*")
    """
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)
{% else -%}
# Redis dependencies disabled - Redis not enabled
{% endif %}

{% if cookiecutter.include_auth == "yes" -%}
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"id": user_id}
    except JWTError:
        raise credentials_exception
{% else -%}
# Authentication dependencies disabled - Auth not enabled
{% endif -%}
