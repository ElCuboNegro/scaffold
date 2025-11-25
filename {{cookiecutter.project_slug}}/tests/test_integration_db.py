{% if cookiecutter.use_postgresql == "yes" -%}
"""End-to-end integration tests with database."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from app.models.example import Example

# Create test database engine
SQLALCHEMY_TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/{{ cookiecutter.database_name }}", "/{{ cookiecutter.database_name }}_test"
)

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


def test_create_and_retrieve_example(client: TestClient, db_session: Session) -> None:
    """Test creating an example and retrieving it from database."""
    # Create an example via API
    example_data = {
        "name": "Integration Test Example",
        "description": "Testing database integration",
    }
    
    response = client.post("/api/v1/example/", json=example_data)
    assert response.status_code == 201
    created_example = response.json()
    example_id = created_example["id"]
    
    # Verify it was saved to database
    db_example = db_session.query(Example).filter(Example.id == example_id).first()
    assert db_example is not None
    assert db_example.name == example_data["name"]
    assert db_example.description == example_data["description"]
    
    # Retrieve via API
    response = client.get(f"/api/v1/example/{example_id}")
    assert response.status_code == 200
    retrieved_example = response.json()
    assert retrieved_example["id"] == example_id
    assert retrieved_example["name"] == example_data["name"]


def test_list_examples_from_database(client: TestClient, db_session: Session) -> None:
    """Test listing examples populated in database."""
    # Create test data directly in database
    examples = [
        Example(name="Example 1", description="First example"),
        Example(name="Example 2", description="Second example"),
        Example(name="Example 3", description="Third example"),
    ]
    
    for example in examples:
        db_session.add(example)
    db_session.commit()
    
    # Retrieve via API
    response = client.get("/api/v1/example/")
    assert response.status_code == 200
    
    retrieved_examples = response.json()
    assert len(retrieved_examples) == 3
    assert all(ex["name"] in ["Example 1", "Example 2", "Example 3"] for ex in retrieved_examples)


def test_update_example_in_database(client: TestClient, db_session: Session) -> None:
    """Test updating an example in the database."""
    # Create initial example
    example = Example(name="Original Name", description="Original description")
    db_session.add(example)
    db_session.commit()
    db_session.refresh(example)
    
    # Update via API
    update_data = {
        "name": "Updated Name",
        "description": "Updated description",
    }
    
    response = client.put(f"/api/v1/example/{example.id}", json=update_data)
    assert response.status_code == 200
    
    # Verify in database
    db_session.refresh(example)
    assert example.name == "Updated Name"
    assert example.description == "Updated description"


def test_delete_example_from_database(client: TestClient, db_session: Session) -> None:
    """Test deleting an example from the database."""
    # Create example
    example = Example(name="To Delete", description="This will be deleted")
    db_session.add(example)
    db_session.commit()
    example_id = example.id
    
    # Delete via API
    response = client.delete(f"/api/v1/example/{example_id}")
    assert response.status_code == 200
    
    # Verify it's gone from database
    deleted_example = db_session.query(Example).filter(Example.id == example_id).first()
    assert deleted_example is None


def test_database_transaction_rollback(client: TestClient, db_session: Session) -> None:
    """Test that failed operations don't corrupt the database."""
    # Create a valid example
    example = Example(name="Valid Example", description="Should persist")
    db_session.add(example)
    db_session.commit()
    
    # Attempt to create an invalid example (e.g., missing required field)
    invalid_data = {"description": "Missing name field"}
    
    response = client.post("/api/v1/example/", json=invalid_data)
    assert response.status_code == 422  # Validation error
    
    # Verify the valid example still exists
    examples = db_session.query(Example).all()
    assert len(examples) == 1
    assert examples[0].name == "Valid Example"


def test_concurrent_database_operations(client: TestClient, db_session: Session) -> None:
    """Test multiple concurrent database operations."""
    # Create multiple examples
    example_data_list = [
        {"name": f"Example {i}", "description": f"Description {i}"}
        for i in range(10)
    ]
    
    created_ids = []
    for data in example_data_list:
        response = client.post("/api/v1/example/", json=data)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])
    
    # Verify all were created
    examples = db_session.query(Example).all()
    assert len(examples) == 10
    
    # Verify we can retrieve each one
    for example_id in created_ids:
        response = client.get(f"/api/v1/example/{example_id}")
        assert response.status_code == 200
{% else -%}
"""End-to-end integration tests (database not enabled)."""

# Database integration tests are only available when PostgreSQL is enabled
# To enable, regenerate the project with use_postgresql=yes
{% endif -%}
