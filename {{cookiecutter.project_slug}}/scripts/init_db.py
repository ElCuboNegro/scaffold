"""Database initialization script.

This script creates the database if it doesn't exist.
Safe to run multiple times - will skip if database already exists.
"""

import asyncio
import sys
from urllib.parse import urlparse

import asyncpg
from asyncpg.exceptions import InvalidCatalogNameError

from app.core.config import settings


async def create_database_if_not_exists() -> None:
    """Create the database if it doesn't exist."""
    # Parse the database URL to extract components
    parsed = urlparse(settings.DATABASE_URL.replace("+asyncpg", ""))

    database_name = parsed.path.lstrip("/")
    username = parsed.username or "postgres"
    password = parsed.password or "postgres"
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432

    # Connection URL to postgres database (for administrative tasks)
    admin_url = f"postgresql://{username}:{password}@{host}:{port}/postgres"

    print(f"Checking if database '{database_name}' exists...")

    try:
        # Try to connect to the target database
        conn = await asyncpg.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=database_name,
        )
        await conn.close()
        print(f"✓ Database '{database_name}' already exists.")
        return
    except InvalidCatalogNameError:
        # Database doesn't exist, create it
        print(f"Database '{database_name}' does not exist. Creating...")
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        sys.exit(1)

    try:
        # Connect to postgres database to create the new database
        conn = await asyncpg.connect(admin_url)

        # Create the database
        await conn.execute(f'CREATE DATABASE "{database_name}"')
        await conn.close()

        print(f"✓ Database '{database_name}' created successfully!")
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)

    try:
        asyncio.run(create_database_if_not_exists())
        print("\n✓ Database initialization completed successfully!")
    except KeyboardInterrupt:
        print("\n✗ Database initialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
