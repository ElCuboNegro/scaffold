{% if cookiecutter.include_auth == "yes" -%}
"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base schema for User."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100, description="User password")


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    """Schema for user response."""

    id: int = Field(..., description="User ID")

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: str | None = None
{% else -%}
"""Authentication schemas placeholder - Auth not enabled."""

# Authentication schemas disabled in this configuration
# To enable, regenerate with include_auth=yes
{% endif -%}
