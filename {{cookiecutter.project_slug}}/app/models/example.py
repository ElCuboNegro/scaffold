{% if cookiecutter.use_postgresql == "yes" -%}
"""Example SQLAlchemy model."""

from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Example(Base):
    """Example model demonstrating SQLAlchemy ORM."""

    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Example(id={self.id}, name='{self.name}')>"
{% else -%}
"""Models placeholder - PostgreSQL not enabled."""

# Database models disabled in this configuration
# To enable, regenerate with use_postgresql=yes
{% endif -%}
