{% if cookiecutter.use_postgresql == "yes" and cookiecutter.include_auth == "yes" -%}
"""User SQLAlchemy model for authentication."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Integer, default=1, nullable=False)

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
{% else -%}
"""User model placeholder - PostgreSQL or Auth not enabled."""

# User model disabled in this configuration
# To enable, regenerate with use_postgresql=yes and include_auth=yes
{% endif -%}
