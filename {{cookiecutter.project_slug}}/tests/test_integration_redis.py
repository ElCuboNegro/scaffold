{% if cookiecutter.use_redis == "yes" -%}
"""End-to-end integration tests with Redis."""

import json
import time

import pytest
import redis
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def redis_client() -> redis.Redis:
    """Create a Redis client for testing."""
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    # Clear test keys before each test
    for key in r.scan_iter("test:*"):
        r.delete(key)
    
    yield r
    
    # Clean up after test
    for key in r.scan_iter("test:*"):
        r.delete(key)


def test_redis_connection(redis_client: redis.Redis) -> None:
    """Test basic Redis connectivity."""
    # Test ping
    assert redis_client.ping() is True
    
    # Test set/get
    redis_client.set("test:connection", "working")
    assert redis_client.get("test:connection") == "working"


def test_redis_caching_example(redis_client: redis.Redis) -> None:
    """Test caching example data in Redis."""
    cache_key = "test:example:1"
    example_data = {
        "id": 1,
        "name": "Cached Example",
        "description": "This is cached in Redis",
    }
    
    # Cache the data
    redis_client.setex(
        cache_key,
        3600,  # 1 hour TTL
        json.dumps(example_data)
    )
    
    # Retrieve from cache
    cached_data = redis_client.get(cache_key)
    assert cached_data is not None
    
    retrieved_data = json.loads(cached_data)
    assert retrieved_data["id"] == example_data["id"]
    assert retrieved_data["name"] == example_data["name"]


def test_redis_cache_expiration(redis_client: redis.Redis) -> None:
    """Test that Redis cache expires correctly."""
    cache_key = "test:expiring:key"
    
    # Set with 1 second TTL
    redis_client.setex(cache_key, 1, "temporary_value")
    
    # Verify it exists
    assert redis_client.get(cache_key) == "temporary_value"
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Verify it's gone
    assert redis_client.get(cache_key) is None


def test_redis_list_operations(redis_client: redis.Redis) -> None:
    """Test Redis list operations for queue-like behavior."""
    queue_key = "test:task:queue"
    
    # Push tasks to queue
    tasks = ["task1", "task2", "task3"]
    for task in tasks:
        redis_client.rpush(queue_key, task)
    
    # Verify queue length
    assert redis_client.llen(queue_key) == 3
    
    # Pop tasks from queue (FIFO)
    popped_tasks = []
    while redis_client.llen(queue_key) > 0:
        task = redis_client.lpop(queue_key)
        popped_tasks.append(task)
    
    assert popped_tasks == tasks


def test_redis_hash_operations(redis_client: redis.Redis) -> None:
    """Test Redis hash operations for structured data."""
    user_key = "test:user:123"
    
    # Store user data as hash
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "admin",
    }
    
    redis_client.hset(user_key, mapping=user_data)
    
    # Retrieve individual fields
    assert redis_client.hget(user_key, "name") == "John Doe"
    assert redis_client.hget(user_key, "email") == "john@example.com"
    
    # Retrieve all fields
    retrieved_data = redis_client.hgetall(user_key)
    assert retrieved_data == user_data


def test_redis_set_operations(redis_client: redis.Redis) -> None:
    """Test Redis set operations for unique collections."""
    tags_key = "test:post:tags"
    
    # Add tags
    tags = ["python", "fastapi", "redis", "testing"]
    for tag in tags:
        redis_client.sadd(tags_key, tag)
    
    # Verify set size
    assert redis_client.scard(tags_key) == 4
    
    # Check membership
    assert redis_client.sismember(tags_key, "python") is True
    assert redis_client.sismember(tags_key, "java") is False
    
    # Get all members
    all_tags = redis_client.smembers(tags_key)
    assert all_tags == set(tags)


def test_redis_sorted_set_leaderboard(redis_client: redis.Redis) -> None:
    """Test Redis sorted set for leaderboard functionality."""
    leaderboard_key = "test:leaderboard"
    
    # Add scores
    scores = {
        "player1": 100,
        "player2": 250,
        "player3": 175,
        "player4": 300,
    }
    
    for player, score in scores.items():
        redis_client.zadd(leaderboard_key, {player: score})
    
    # Get top 3 players (highest scores)
    top_players = redis_client.zrevrange(leaderboard_key, 0, 2, withscores=True)
    
    assert len(top_players) == 3
    assert top_players[0][0] == "player4"  # Highest score
    assert top_players[0][1] == 300
    
    # Get player rank
    rank = redis_client.zrevrank(leaderboard_key, "player2")
    assert rank == 2  # 3rd place (0-indexed)


def test_redis_pub_sub_messaging(redis_client: redis.Redis) -> None:
    """Test Redis pub/sub for real-time messaging."""
    channel = "test:notifications"
    
    # Create subscriber
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    
    # Skip the subscription confirmation message
    message = pubsub.get_message()
    assert message is not None
    assert message["type"] == "subscribe"
    
    # Publish a message
    test_message = "Hello, Redis!"
    redis_client.publish(channel, test_message)
    
    # Receive the message
    time.sleep(0.1)  # Small delay for message propagation
    message = pubsub.get_message()
    
    assert message is not None
    assert message["type"] == "message"
    assert message["data"] == test_message
    
    # Clean up
    pubsub.unsubscribe(channel)
    pubsub.close()


def test_redis_atomic_increment(redis_client: redis.Redis) -> None:
    """Test Redis atomic operations for counters."""
    counter_key = "test:page:views"
    
    # Increment counter multiple times
    for _ in range(10):
        redis_client.incr(counter_key)
    
    # Verify final count
    count = redis_client.get(counter_key)
    assert int(count) == 10
    
    # Decrement
    redis_client.decr(counter_key)
    assert int(redis_client.get(counter_key)) == 9


def test_redis_pipeline_batch_operations(redis_client: redis.Redis) -> None:
    """Test Redis pipeline for batch operations."""
    # Use pipeline for multiple operations
    pipe = redis_client.pipeline()
    
    for i in range(5):
        pipe.set(f"test:batch:{i}", f"value_{i}")
    
    # Execute all at once
    results = pipe.execute()
    assert len(results) == 5
    assert all(result is True for result in results)
    
    # Verify all keys were set
    for i in range(5):
        value = redis_client.get(f"test:batch:{i}")
        assert value == f"value_{i}"
{% else -%}
"""End-to-end integration tests (Redis not enabled)."""

# Redis integration tests are only available when Redis is enabled
# To enable, regenerate the project with use_redis=yes
{% endif -%}
