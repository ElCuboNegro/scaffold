Feature: End-to-End Celery Integration
  As a developer
  I want to test background task processing
  So that I can ensure async operations work correctly

  Scenario: Process background task
    Given the Celery worker is running
    When I trigger a background task via API
    Then the task should be queued
    And the task should complete successfully
    And I should be able to retrieve the task result

  Scenario: Handle task failures gracefully
    Given the Celery worker is running
    When I trigger a task that will fail
    Then the task should retry automatically
    And eventually return a failure status

  Scenario: Process multiple tasks concurrently
    Given the Celery worker is running
    When I trigger 10 background tasks simultaneously
    Then all tasks should be queued
    And all tasks should complete within 30 seconds
