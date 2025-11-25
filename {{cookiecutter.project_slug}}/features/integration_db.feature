Feature: End-to-End Database Integration
  As a developer
  I want to test full database workflows
  So that I can ensure data persistence works correctly

  {% if cookiecutter.use_postgresql == "yes" -%}
  Scenario: Complete CRUD workflow
    Given the database is empty
    When I create a new example via API
    Then the example should be stored in the database
    And I should be able to retrieve it by ID
    And I should be able to update it
    And I should be able to delete it
    And it should no longer exist in the database

  Scenario: Bulk data operations
    Given the database is empty
    When I create 10 examples via API
    Then all 10 examples should be in the database
    And I should be able to list all of them
    And I should be able to filter them by name

  Scenario: Database transaction integrity
    Given the database has 5 examples
    When I attempt to create an invalid example
    Then the operation should fail
    And the existing 5 examples should remain unchanged
  {% else -%}
  # Database integration scenarios require PostgreSQL
  # To enable, regenerate with use_postgresql=yes
  {% endif -%}
