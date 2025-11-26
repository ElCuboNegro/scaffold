{% if cookiecutter.use_postgresql == "yes" -%}
"""CRUD operations for Example model."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate


async def get_example(db: AsyncSession, example_id: int) -> Example | None:
    """Get an example by ID."""
    result = await db.execute(select(Example).where(Example.id == example_id))
    return result.scalar_one_or_none()


async def get_examples(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Example]:
    """Get a list of examples."""
    result = await db.execute(select(Example).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_example(db: AsyncSession, example: ExampleCreate) -> Example:
    """Create a new example."""
    db_example = Example(
        name=example.name,
        description=example.description,
    )
    db.add(db_example)
    await db.commit()
    await db.refresh(db_example)
    return db_example


async def update_example(
    db: AsyncSession,
    example_id: int,
    example: ExampleUpdate,
) -> Example | None:
    """Update an existing example."""
    db_example = await get_example(db, example_id)
    if not db_example:
        return None

    update_data = example.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_example, field, value)

    await db.commit()
    await db.refresh(db_example)
    return db_example


async def delete_example(db: AsyncSession, example_id: int) -> bool:
    """Delete an example."""
    db_example = await get_example(db, example_id)
    if not db_example:
        return False

    await db.delete(db_example)
    await db.commit()
    return True
{% else -%}
"""CRUD placeholder - PostgreSQL not enabled."""

# CRUD operations disabled in this configuration
# To enable, regenerate with use_postgresql=yes
{% endif -%}
