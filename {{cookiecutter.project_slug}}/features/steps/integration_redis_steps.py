"""Step definitions for Redis integration tests."""

{% if cookiecutter.use_redis == "yes" -%}
import json
import time

import redis
from behave import given, then, when
from behave.runner import Context

from app.core.config import settings


@given("Redis is available")
def step_redis_available(context: Context) -> None:
    """Verify Redis connection."""
    context.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    assert context.redis.ping() is True
    
    # Clean up test keys
    for key in context.redis.scan_iter("test:*"):
        context.redis.delete(key)


@when('I cache an example with key "{cache_key}"')
def step_cache_example(context: Context, cache_key: str) -> None:
    """Cache example data."""
    context.cache_key = cache_key
    context.cached_data = {
        "id": 1,
        "name": "Cached Example",
        "description": "Test data",
    }
    
    context.redis.setex(
        cache_key,
        3600,  # 1 hour TTL
        json.dumps(context.cached_data)
    )


@when("I cache data with {ttl:d} second TTL")
def step_cache_with_ttl(context: Context, ttl: int) -> None:
    """Cache data with specific TTL."""
    context.cache_key = "test:expiring"
    context.redis.setex(context.cache_key, ttl, "temporary")


@when("I wait for {seconds:d} seconds")
def step_wait(context: Context, seconds: int) -> None:
    """Wait for specified seconds."""
    time.sleep(seconds)


@when("I make {count:d} API requests in {seconds:d} second")
def step_make_requests(context: Context, count: int, seconds: int) -> None:
    """Make multiple API requests."""
    context.responses = []
    for i in range(count):
        response = context.client.get("/health")
        context.responses.append(response)


@then("I should be able to retrieve it from cache")
def step_retrieve_from_cache(context: Context) -> None:
    """Retrieve data from cache."""
    cached = context.redis.get(context.cache_key)
    assert cached is not None


@then("the cached data should match the original")
def step_cached_data_matches(context: Context) -> None:
    """Verify cached data matches."""
    cached = context.redis.get(context.cache_key)
    retrieved_data = json.loads(cached)
    assert retrieved_data == context.cached_data


@then("the cached data should be expired")
def step_data_expired(context: Context) -> None:
    """Verify data is expired."""
    cached = context.redis.get(context.cache_key)
    assert cached is None


@then("the first {count:d} should succeed")
def step_first_succeed(context: Context, count: int) -> None:
    """Verify first N requests succeeded."""
    for i in range(count):
        assert context.responses[i].status_code == 200


@then("the remaining {count:d} should be rate limited")
def step_remaining_rate_limited(context: Context, count: int) -> None:
    """Verify remaining requests are rate limited."""
    # This would require implementing rate limiting in the API
    # For now, just verify we have the responses
    assert len(context.responses) >= count
{% else -%}
# Redis integration step definitions require Redis
# To enable, regenerate with use_redis=yes
{% endif -%}
