{% if cookiecutter.use_postgresql == "yes" and cookiecutter.include_auth == "yes" -%}
"""CRUD operations for User model."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """Get a user by ID."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get a user by email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Get a user by username."""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    """
    Authenticate a user by username/email and password.

    Args:
        db: Database session
        username: Username or email
        password: Plain text password

    Returns:
        User if authentication successful, None otherwise
    """
    # Try to find user by username or email
    user = await get_user_by_username(db, username)
    if not user:
        user = await get_user_by_email(db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
{% else -%}
"""User CRUD placeholder - PostgreSQL or Auth not enabled."""

# User CRUD operations disabled in this configuration
# To enable, regenerate with use_postgresql=yes and include_auth=yes
{% endif -%}
