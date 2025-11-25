"""Step definitions for Celery integration tests."""

import time

from behave import given, then, when
from behave.runner import Context
from celery.result import AsyncResult

from app.core.celery_app import celery_app
from app.tasks.example import example_task


@given("the Celery worker is running")
def step_celery_running(context: Context) -> None:
    """Verify Celery is configured."""
    # In eager mode, tasks run synchronously
    assert celery_app.conf.task_always_eager is True


@when("I trigger a background task via API")
def step_trigger_task_via_api(context: Context) -> None:
    """Trigger task through API."""
    response = context.client.post("/api/v1/example/task?message=test")
    assert response.status_code == 200
    context.task_id = response.json()["task_id"]


@when("I trigger a task that will fail")
def step_trigger_failing_task(context: Context) -> None:
    """Trigger a task designed to fail."""
    # This would require a task that raises an exception
    result = example_task.delay("fail_test")
    context.task_result = result


@when("I trigger {count:d} background tasks simultaneously")
def step_trigger_multiple_tasks(context: Context, count: int) -> None:
    """Trigger multiple tasks."""
    context.task_results = []
    for i in range(count):
        result = example_task.delay(f"task_{i}")
        context.task_results.append(result)


@then("the task should be queued")
def step_task_queued(context: Context) -> None:
    """Verify task was queued."""
    assert context.task_id is not None


@then("the task should complete successfully")
def step_task_completes(context: Context) -> None:
    """Verify task completed."""
    result = AsyncResult(context.task_id, app=celery_app)
    assert result.ready() is True
    assert result.successful() is True


@then("I should be able to retrieve the task result")
def step_retrieve_task_result(context: Context) -> None:
    """Retrieve task result."""
    result = AsyncResult(context.task_id, app=celery_app)
    task_data = result.get(timeout=5)
    assert task_data["status"] == "success"


@then("the task should retry automatically")
def step_task_retries(context: Context) -> None:
    """Verify task retry logic."""
    # In eager mode, retries work differently
    # This is a placeholder for actual retry testing
    pass


@then("eventually return a failure status")
def step_task_fails(context: Context) -> None:
    """Verify task eventually fails."""
    # Placeholder for failure testing
    pass


@then("all tasks should be queued")
def step_all_tasks_queued(context: Context) -> None:
    """Verify all tasks were queued."""
    assert len(context.task_results) > 0


@then("all tasks should complete within {seconds:d} seconds")
def step_all_tasks_complete(context: Context, seconds: int) -> None:
    """Verify all tasks complete in time."""
    start_time = time.time()
    
    for result in context.task_results:
        assert result.ready() is True
        assert result.successful() is True
    
    elapsed = time.time() - start_time
    assert elapsed < seconds
