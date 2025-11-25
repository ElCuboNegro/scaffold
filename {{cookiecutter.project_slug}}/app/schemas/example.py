"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field


class ExampleBase(BaseModel):
    """Base schema for Example."""

    name: str = Field(..., min_length=1, max_length=100, description="Example name")
    description: str | None = Field(None, max_length=500, description="Example description")


class ExampleCreate(ExampleBase):
    """Schema for creating an Example."""

    pass


class ExampleUpdate(BaseModel):
    """Schema for updating an Example."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class ExampleResponse(ExampleBase):
    """Schema for Example response."""

    id: int = Field(..., description="Example ID")

    model_config = {"from_attributes": True}
