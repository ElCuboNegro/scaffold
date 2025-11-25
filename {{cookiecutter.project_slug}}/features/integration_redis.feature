Feature: End-to-End Redis Integration
  As a developer
  I want to test Redis caching and data structures
  So that I can ensure caching works correctly

  {% if cookiecutter.use_redis == "yes" -%}
  Scenario: Cache example data
    Given Redis is available
    When I cache an example with key "test:example:1"
    Then I should be able to retrieve it from cache
    And the cached data should match the original

  Scenario: Cache expiration
    Given Redis is available
    When I cache data with 1 second TTL
    And I wait for 2 seconds
    Then the cached data should be expired

  Scenario: Use Redis for rate limiting
    Given Redis is available
    When I make 5 API requests in 1 second
    Then the first 3 should succeed
    And the remaining 2 should be rate limited
  {% else -%}
  # Redis integration scenarios require Redis
  # To enable, regenerate with use_redis=yes
  {% endif -%}
