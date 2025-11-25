{% if cookiecutter.use_postgresql == "yes" -%}
"""CRUD operations for Example model."""

from sqlalchemy.orm import Session

from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate


def get_example(db: Session, example_id: int) -> Example | None:
    """Get an example by ID."""
    return db.query(Example).filter(Example.id == example_id).first()


def get_examples(db: Session, skip: int = 0, limit: int = 100) -> list[Example]:
    """Get a list of examples."""
    return db.query(Example).offset(skip).limit(limit).all()


def create_example(db: Session, example: ExampleCreate) -> Example:
    """Create a new example."""
    db_example = Example(
        name=example.name,
        description=example.description,
    )
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example


def update_example(
    db: Session,
    example_id: int,
    example: ExampleUpdate,
) -> Example | None:
    """Update an existing example."""
    db_example = get_example(db, example_id)
    if not db_example:
        return None

    update_data = example.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_example, field, value)

    db.commit()
    db.refresh(db_example)
    return db_example


def delete_example(db: Session, example_id: int) -> bool:
    """Delete an example."""
    db_example = get_example(db, example_id)
    if not db_example:
        return False

    db.delete(db_example)
    db.commit()
    return True
{% else -%}
"""CRUD placeholder - PostgreSQL not enabled."""

# CRUD operations disabled in this configuration
# To enable, regenerate with use_postgresql=yes
{% endif -%}
