"""Step definitions for database integration tests."""

{% if cookiecutter.use_postgresql == "yes" -%}
from behave import given, then, when
from behave.runner import Context
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models.example import Example

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/{{ cookiecutter.database_name }}", "/{{ cookiecutter.database_name }}_test"
)
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@given("the database is empty")
def step_database_empty(context: Context) -> None:
    """Ensure database is empty."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    context.db = TestingSessionLocal()


@given("the database has {count:d} examples")
def step_database_has_examples(context: Context, count: int) -> None:
    """Populate database with examples."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    context.db = TestingSessionLocal()
    
    for i in range(count):
        example = Example(name=f"Example {i+1}", description=f"Description {i+1}")
        context.db.add(example)
    context.db.commit()


@when("I create a new example via API")
def step_create_example_via_api(context: Context) -> None:
    """Create example through API."""
    example_data = {
        "name": "Test Example",
        "description": "Created via API",
    }
    context.response = context.client.post("/api/v1/example/", json=example_data)
    context.created_id = context.response.json().get("id")


@when("I create {count:d} examples via API")
def step_create_multiple_examples(context: Context, count: int) -> None:
    """Create multiple examples via API."""
    context.created_ids = []
    for i in range(count):
        example_data = {
            "name": f"Bulk Example {i+1}",
            "description": f"Bulk Description {i+1}",
        }
        response = context.client.post("/api/v1/example/", json=example_data)
        context.created_ids.append(response.json()["id"])


@when("I attempt to create an invalid example")
def step_create_invalid_example(context: Context) -> None:
    """Attempt to create invalid example."""
    invalid_data = {"description": "Missing name field"}
    context.response = context.client.post("/api/v1/example/", json=invalid_data)


@then("the example should be stored in the database")
def step_example_in_database(context: Context) -> None:
    """Verify example is in database."""
    example = context.db.query(Example).filter(Example.id == context.created_id).first()
    assert example is not None
    assert example.name == "Test Example"


@then("all {count:d} examples should be in the database")
def step_all_examples_in_database(context: Context, count: int) -> None:
    """Verify all examples are in database."""
    examples = context.db.query(Example).all()
    assert len(examples) == count


@then("I should be able to retrieve it by ID")
def step_retrieve_by_id(context: Context) -> None:
    """Retrieve example by ID."""
    response = context.client.get(f"/api/v1/example/{context.created_id}")
    assert response.status_code == 200
    assert response.json()["id"] == context.created_id


@then("I should be able to update it")
def step_update_example(context: Context) -> None:
    """Update the example."""
    update_data = {
        "name": "Updated Name",
        "description": "Updated Description",
    }
    response = context.client.put(f"/api/v1/example/{context.created_id}", json=update_data)
    assert response.status_code == 200


@then("I should be able to delete it")
def step_delete_example(context: Context) -> None:
    """Delete the example."""
    response = context.client.delete(f"/api/v1/example/{context.created_id}")
    assert response.status_code == 200


@then("it should no longer exist in the database")
def step_example_not_in_database(context: Context) -> None:
    """Verify example is deleted."""
    example = context.db.query(Example).filter(Example.id == context.created_id).first()
    assert example is None


@then("I should be able to list all of them")
def step_list_all_examples(context: Context) -> None:
    """List all examples."""
    response = context.client.get("/api/v1/example/")
    assert response.status_code == 200
    examples = response.json()
    assert len(examples) == len(context.created_ids)


@then("I should be able to filter them by name")
def step_filter_by_name(context: Context) -> None:
    """Filter examples by name."""
    response = context.client.get("/api/v1/example/?name=Bulk Example 1")
    assert response.status_code == 200


@then("the operation should fail")
def step_operation_fails(context: Context) -> None:
    """Verify operation failed."""
    assert context.response.status_code == 422


@then("the existing {count:d} examples should remain unchanged")
def step_examples_unchanged(context: Context, count: int) -> None:
    """Verify existing examples unchanged."""
    examples = context.db.query(Example).all()
    assert len(examples) == count
{% else -%}
# Database integration step definitions require PostgreSQL
# To enable, regenerate with use_postgresql=yes
{% endif -%}
