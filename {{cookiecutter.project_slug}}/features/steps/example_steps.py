"""Step definitions for example feature."""

from behave import given, then, when
from behave.runner import Context


@given("the API is running")
def step_api_running(context: Context) -> None:
    """Verify the API client is available."""
    assert context.client is not None


@when('I send a GET request to "{endpoint}"')
def step_get_request(context: Context, endpoint: str) -> None:
    """Send a GET request to the specified endpoint."""
    context.response = context.client.get(endpoint)


@when('I send a POST request to "{endpoint}"')
def step_post_request_simple(context: Context, endpoint: str) -> None:
    """Send a POST request to the specified endpoint."""
    context.response = context.client.post(endpoint)


@when('I send a POST request to "{endpoint}" with')
def step_post_request_with_data(context: Context, endpoint: str) -> None:
    """Send a POST request with table data."""
    # Get the first row of data from the table
    row = context.table[0]
    
    # Construct the proper request body
    request_body = {
        "name": row["name"],
        "description": row["description"],
    }

    context.response = context.client.post(endpoint, json=request_body)


@then("the response status code should be {status_code:d}")
def step_check_status_code(context: Context, status_code: int) -> None:
    """Verify the response status code."""
    assert context.response.status_code == status_code, (
        f"Expected {status_code}, got {context.response.status_code}. "
        f"Response: {context.response.text}"
    )


@then('the response should contain "{field}"')
def step_response_contains_field(context: Context, field: str) -> None:
    """Verify the response contains a specific field."""
    response_data = context.response.json()
    assert field in response_data, f"Field '{field}' not found in response: {response_data}"


@then("the response should be a list")
def step_response_is_list(context: Context) -> None:
    """Verify the response is a list."""
    response_data = context.response.json()
    assert isinstance(response_data, list), f"Expected list, got {type(response_data)}"

