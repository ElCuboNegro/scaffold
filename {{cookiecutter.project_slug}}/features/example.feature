Feature: Example API
  As an API consumer
  I want to interact with the example endpoints
  So that I can manage example resources

  Scenario: Health check endpoint
    Given the API is running
    When I send a GET request to "/health"
    Then the response status code should be 200
    And the response should contain "status"

  Scenario: List examples
    Given the API is running
    When I send a GET request to "/api/v1/example/"
    Then the response status code should be 200
    And the response should be a list

  Scenario: Create an example
    Given the API is running
    When I send a POST request to "/api/v1/example/" with:
      | name       | description        |
      | Test Item  | A test description |
    Then the response status code should be 201
    And the response should contain "id"
    And the response should contain "name"

  Scenario: Trigger a background task
    Given the API is running
    When I send a POST request to "/api/v1/example/task?message=test"
    Then the response status code should be 200
    And the response should contain "task_id"
    And the response should contain "status"
