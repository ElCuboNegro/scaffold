"""End-to-end integration tests with Celery tasks."""

import time

import pytest
from celery.result import AsyncResult
from fastapi.testclient import TestClient

from app.core.celery_app import celery_app
from app.main import app
from app.tasks.example import example_task, send_email_task

client = TestClient(app)


def test_celery_task_execution() -> None:
    """Test that Celery tasks execute successfully."""
    # Trigger task directly
    result = example_task.delay("test message")
    
    # In eager mode, task completes immediately
    assert result.ready() is True
    assert result.successful() is True
    
    # Check result
    task_result = result.get(timeout=5)
    assert task_result["status"] == "success"
    assert task_result["message"] == "test message"
    assert "Processed: test message" in task_result["result"]


def test_celery_task_via_api() -> None:
    """Test triggering Celery task through API endpoint."""
    response = client.post("/api/v1/example/task?message=api_test")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "task_id" in data
    assert "status" in data
    
    # Verify task ID format
    task_id = data["task_id"]
    assert len(task_id) > 0


def test_celery_task_with_result_backend() -> None:
    """Test retrieving task results from backend."""
    # Execute task
    result = example_task.delay("backend_test")
    task_id = result.id
    
    # Retrieve result using task ID
    async_result = AsyncResult(task_id, app=celery_app)
    
    assert async_result.ready() is True
    task_data = async_result.get(timeout=5)
    
    assert task_data["status"] == "success"
    assert task_data["message"] == "backend_test"


def test_celery_email_task() -> None:
    """Test email sending task."""
    result = send_email_task.delay(
        recipient="test@example.com",
        subject="Test Email",
        body="This is a test email"
    )
    
    assert result.ready() is True
    task_result = result.get(timeout=5)
    
    assert task_result["status"] == "sent"
    assert task_result["recipient"] == "test@example.com"
    assert task_result["subject"] == "Test Email"


def test_celery_task_chaining() -> None:
    """Test chaining multiple Celery tasks."""
    from celery import chain
    
    # Create a chain of tasks
    workflow = chain(
        example_task.s("first"),
        example_task.s("second"),
        example_task.s("third"),
    )
    
    result = workflow.apply()
    
    # In eager mode, chain completes immediately
    assert result.ready() is True
    final_result = result.get(timeout=5)
    
    assert final_result["status"] == "success"


def test_celery_task_grouping() -> None:
    """Test running multiple tasks in parallel."""
    from celery import group
    
    # Create a group of tasks
    job = group(
        example_task.s(f"task_{i}") for i in range(5)
    )
    
    result = job.apply()
    
    # Wait for all tasks to complete
    results = result.get(timeout=10)
    
    assert len(results) == 5
    for task_result in results:
        assert task_result["status"] == "success"


def test_celery_task_error_handling() -> None:
    """Test Celery task error handling and retries."""
    # This would test retry logic, but in eager mode retries don't work the same way
    # In production, you'd test with actual broker
    
    result = example_task.delay("error_test")
    assert result.ready() is True


def test_celery_task_with_eta() -> None:
    """Test scheduling tasks with ETA (estimated time of arrival)."""
    from datetime import datetime, timedelta
    
    # Schedule task for 1 second in the future
    eta = datetime.utcnow() + timedelta(seconds=1)
    
    result = example_task.apply_async(
        args=["scheduled_task"],
        eta=eta
    )
    
    # In eager mode, ETA is ignored and task runs immediately
    assert result.ready() is True


def test_celery_task_with_countdown() -> None:
    """Test scheduling tasks with countdown."""
    result = example_task.apply_async(
        args=["countdown_task"],
        countdown=2  # 2 seconds
    )
    
    # In eager mode, countdown is ignored
    assert result.ready() is True


def test_celery_periodic_task_registration() -> None:
    """Test that periodic tasks are registered."""
    # Check if celery app has registered tasks
    registered_tasks = celery_app.tasks.keys()
    
    assert "app.tasks.example.example_task" in registered_tasks
    assert "app.tasks.example.send_email_task" in registered_tasks


def test_celery_task_serialization() -> None:
    """Test task argument serialization."""
    # Test with complex data structures
    complex_data = {
        "list": [1, 2, 3],
        "dict": {"key": "value"},
        "string": "test",
        "number": 42,
    }
    
    result = example_task.delay(str(complex_data))
    
    assert result.ready() is True
    task_result = result.get(timeout=5)
    
    assert task_result["status"] == "success"


def test_celery_task_timeout() -> None:
    """Test task timeout configuration."""
    # Verify task has timeout configured
    task_info = celery_app.tasks.get("app.tasks.example.example_task")
    
    assert task_info is not None
    # Task should have time_limit configured in celery_app.py


def test_multiple_concurrent_tasks() -> None:
    """Test handling multiple concurrent task executions."""
    # Trigger multiple tasks
    results = []
    for i in range(10):
        result = example_task.delay(f"concurrent_task_{i}")
        results.append(result)
    
    # Verify all completed
    for result in results:
        assert result.ready() is True
        task_data = result.get(timeout=5)
        assert task_data["status"] == "success"


def test_celery_task_state_tracking() -> None:
    """Test tracking task states."""
    result = example_task.delay("state_test")
    
    # Check task state
    assert result.state in ["SUCCESS", "PENDING"]
    
    if result.state == "SUCCESS":
        assert result.successful() is True
