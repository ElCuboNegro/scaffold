"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import example
{% if cookiecutter.include_auth == "yes" -%}
from app.api.v1.endpoints import auth
{% endif %}

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(example.router, prefix="/example", tags=["example"])
{% if cookiecutter.include_auth == "yes" -%}
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
{% endif %}

# Add more routers here as you create new endpoints
# api_router.include_router(users.router, prefix="/users", tags=["users"])
