"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Configure async backend for pytest-asyncio."""
    return "asyncio"
