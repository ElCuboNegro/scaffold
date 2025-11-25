"""Behave environment configuration and hooks."""

from typing import Any

from behave.runner import Context
from fastapi.testclient import TestClient

from app.main import app
{% if cookiecutter.use_postgresql == "yes" -%}
from app.core.database import SessionLocal
{% endif %}


def before_all(context: Context) -> None:
    """Run before all tests."""
    context.config.setup_logging()


def before_scenario(context: Context, scenario: Any) -> None:
    """Run before each scenario."""
    # Set up test client
    context.client = TestClient(app)
    {% if cookiecutter.use_postgresql == "yes" -%}
    # Set up database session for tests that need it
    context.db = SessionLocal()
    {% endif %}


def after_scenario(context: Context, scenario: Any) -> None:
    """Run after each scenario."""
    # Clean up if needed
    if hasattr(context, "client"):
        context.client.close()
    {% if cookiecutter.use_postgresql == "yes" -%}
    if hasattr(context, "db"):
        context.db.close()
    {% endif %}


def after_all(context: Context) -> None:
    """Run after all tests."""
    pass

