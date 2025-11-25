{% if cookiecutter.include_auth == "yes" -%}
Feature: End-to-End Authentication
  As a user
  I want to register and authenticate
  So that I can access protected resources

  Scenario: User registration
    Given the API is running
    When I register a new user with:
      | email              | username  | password    |
      | test@example.com   | testuser  | password123 |
    Then the response status code should be 201
    And the response should contain "id"
    And the response should contain "email"
    And the response should contain "username"
    And the response should not contain "password"

  Scenario: User login
    Given the API is running
    And a user exists with username "testuser" and password "password123"
    When I login with username "testuser" and password "password123"
    Then the response status code should be 200
    And the response should contain "access_token"
    And the response should contain "token_type"

  Scenario: Access protected endpoint with valid token
    Given the API is running
    And a user exists with username "testuser" and password "password123"
    And I have a valid access token for "testuser"
    When I access "/api/v1/auth/me" with the token
    Then the response status code should be 200
    And the response should contain "username"
    And the username should be "testuser"

  Scenario: Access protected endpoint without token
    Given the API is running
    When I access "/api/v1/auth/me" without a token
    Then the response status code should be 401

  Scenario: Duplicate email registration
    Given the API is running
    And a user exists with email "test@example.com"
    When I register a new user with:
      | email              | username   | password    |
      | test@example.com   | newuser    | password123 |
    Then the response status code should be 400
    And the response should contain "Email already registered"

  Scenario: Duplicate username registration
    Given the API is running
    And a user exists with username "testuser"
    When I register a new user with:
      | email              | username  | password    |
      | new@example.com    | testuser  | password123 |
    Then the response status code should be 400
    And the response should contain "Username already taken"

  Scenario: Login with invalid credentials
    Given the API is running
    When I login with username "nonexistent" and password "wrongpassword"
    Then the response status code should be 401
{% else -%}
# Authentication scenarios require Auth
# To enable, regenerate with include_auth=yes
{% endif -%}
