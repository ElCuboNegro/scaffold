{% if cookiecutter.include_auth == "yes" -%}
"""Step definitions for authentication integration tests."""

from behave import given, then, when
from behave.runner import Context

from app.core.security import get_password_hash
from app.crud import user as crud
from app.models.user import User
from app.schemas.auth import UserCreate


@given('a user exists with username "{username}" and password "{password}"')
def step_user_exists(context: Context, username: str, password: str) -> None:
    """Create a test user."""
    # Clean up existing user
    existing = crud.get_user_by_username(context.db, username)
    if existing:
        context.db.delete(existing)
        context.db.commit()
    
    # Create new user
    user_in = UserCreate(
        email=f"{username}@example.com",
        username=username,
        password=password,
    )
    crud.create_user(context.db, user_in)


@given('a user exists with email "{email}"')
def step_user_exists_email(context: Context, email: str) -> None:
    """Create a test user with specific email."""
    existing = crud.get_user_by_email(context.db, email)
    if existing:
        return  # User already exists
    
    user_in = UserCreate(
        email=email,
        username=email.split("@")[0],
        password="password123",
    )
    crud.create_user(context.db, user_in)


@given('I have a valid access token for "{username}"')
def step_get_access_token(context: Context, username: str) -> None:
    """Get access token for user."""
    # Login to get token
    response = context.client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "password123"},
    )
    assert response.status_code == 200
    context.access_token = response.json()["access_token"]


@when("I register a new user with")
def step_register_user(context: Context) -> None:
    """Register a new user."""
    row = context.table[0]
    user_data = {
        "email": row["email"],
        "username": row["username"],
        "password": row["password"],
    }
    context.response = context.client.post("/api/v1/auth/register", json=user_data)


@when('I login with username "{username}" and password "{password}"')
def step_login(context: Context, username: str, password: str) -> None:
    """Login with credentials."""
    context.response = context.client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )


@when('I access "{endpoint}" with the token')
def step_access_with_token(context: Context, endpoint: str) -> None:
    """Access endpoint with token."""
    headers = {"Authorization": f"Bearer {context.access_token}"}
    context.response = context.client.get(endpoint, headers=headers)


@when('I access "{endpoint}" without a token')
def step_access_without_token(context: Context, endpoint: str) -> None:
    """Access endpoint without token."""
    context.response = context.client.get(endpoint)


@then('the response should not contain "{field}"')
def step_response_not_contains(context: Context, field: str) -> None:
    """Verify response doesn't contain field."""
    response_data = context.response.json()
    assert field not in response_data, f"Field '{field}' found in response: {response_data}"


@then('the response should contain "{text}"')
def step_response_contains_text(context: Context, text: str) -> None:
    """Verify response contains text."""
    response_text = context.response.text
    assert text in response_text, f"Text '{text}' not found in response: {response_text}"


@then('the username should be "{username}"')
def step_verify_username(context: Context, username: str) -> None:
    """Verify username in response."""
    response_data = context.response.json()
    assert response_data.get("username") == username
{% else -%}
"""Auth step definitions placeholder - Auth not enabled."""

# Authentication step definitions disabled in this configuration
# To enable, regenerate with include_auth=yes
{% endif -%}
