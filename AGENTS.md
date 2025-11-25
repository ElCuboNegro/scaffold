# AGENTS.md - AI Agent Guide for ElCuboNegro Scaffold

## Project Overview

**ElCuboNegro/scaffold** is a production-ready cookiecutter template for building BDD-tested REST APIs with modern Python tooling. This scaffold provides a complete foundation for creating FastAPI applications with Celery task queues, comprehensive BDD testing using Behave, and automated quality assurance through pre-commit hooks and GitHub Actions.

## Purpose

This scaffold eliminates the repetitive setup work required when starting new API projects by providing:

- **FastAPI REST API** - Modern, fast, async-capable web framework with automatic OpenAPI documentation
- **Celery Integration** - Distributed task queue for background jobs and async processing
- **BDD Testing with Behave** - Behavior-Driven Development using Gherkin syntax for readable, business-focused tests
- **Pre-commit Hooks** - Automated code quality checks before commits (linting, formatting, security)
- **GitHub Actions** - CI/CD pipelines for automated testing and deployment
- **Docker Support** - Containerized development and production environments
- **Database Migrations** - Alembic integration for schema version control
- **Configuration Management** - Environment-based settings using Pydantic

## Architecture

### Core Components

```
scaffold/
├── {{cookiecutter.project_slug}}/          # Template root (replaced during generation)
│   ├── app/                                 # FastAPI application
│   │   ├── api/                            # API endpoints and routers
│   │   │   ├── v1/                         # API version 1
│   │   │   │   ├── endpoints/              # Individual endpoint modules
│   │   │   │   └── router.py               # Main router aggregation
│   │   │   └── deps.py                     # Dependency injection
│   │   ├── core/                           # Core functionality
│   │   │   ├── config.py                   # Pydantic settings
│   │   │   ├── security.py                 # Auth & security utilities
│   │   │   └── celery_app.py               # Celery configuration
│   │   ├── models/                         # SQLAlchemy ORM models
│   │   ├── schemas/                        # Pydantic request/response schemas
│   │   ├── crud/                           # Database operations (CRUD)
│   │   ├── tasks/                          # Celery task definitions
│   │   └── main.py                         # FastAPI application factory
│   ├── features/                           # Behave BDD test features
│   │   ├── steps/                          # Step definitions
│   │   └── environment.py                  # Behave hooks and setup
│   ├── tests/                              # Additional unit/integration tests
│   ├── alembic/                            # Database migrations
│   ├── docker/                             # Docker configurations
│   │   ├── Dockerfile                      # Production image
│   │   └── docker-compose.yml              # Local development stack
│   ├── .github/                            # GitHub Actions workflows
│   │   └── workflows/
│   │       ├── ci.yml                      # Continuous Integration
│   │       └── cd.yml                      # Continuous Deployment
│   ├── .pre-commit-config.yaml             # Pre-commit hook configuration
│   ├── pyproject.toml                      # Project metadata & dependencies
│   ├── poetry.lock / requirements.txt      # Locked dependencies
│   └── README.md                           # Project-specific documentation
├── cookiecutter.json                       # Template variables
├── hooks/                                  # Post-generation hooks
│   └── post_gen_project.py                 # Setup automation
├── AGENTS.md                               # This file
└── README.md                               # Scaffold documentation
```

## Technology Stack

### Core Framework
- **FastAPI** - High-performance async web framework
- **Uvicorn** - ASGI server for production
- **Pydantic** - Data validation and settings management
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool

### Task Queue
- **Celery** - Distributed task queue
- **Redis** - Message broker and result backend
- **Flower** - Celery monitoring dashboard (optional)

### Testing
- **Behave** - BDD framework with Gherkin syntax
- **pytest** - Unit and integration testing
- **httpx** - Async HTTP client for API testing
- **coverage** - Code coverage reporting

### Code Quality
- **pre-commit** - Git hook framework
- **ruff** - Fast Python linter and formatter
- **mypy** - Static type checking
- **bandit** - Security vulnerability scanner
- **black** - Code formatter (or ruff format)
- **isort** - Import sorting (or ruff check)

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD automation
- **PostgreSQL** - Production database
- **Redis** - Cache and message broker

## Cookiecutter Variables

When generating a new project from this scaffold, users will be prompted for:

```json
{
  "project_name": "My API Project",
  "project_slug": "my_api_project",
  "project_description": "A FastAPI project with Celery and BDD testing",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "python_version": "3.11",
  "use_docker": "yes",
  "use_postgresql": "yes",
  "use_redis": "yes",
  "include_auth": "yes",
  "license": ["MIT", "Apache-2.0", "GPL-3.0", "Proprietary"]
}
```

## BDD Testing Strategy

### Philosophy: Behavior-Driven Development First

This scaffold follows a **BDD-first testing approach**:

- **Behave (BDD)**: Primary testing method for all user-facing features and integration scenarios
- **pytest**: Secondary, used only for unit testing internal logic and utilities

### Feature Files (Gherkin)

Features are written in natural language using the Given-When-Then pattern:

```gherkin
Feature: User Management
  As an API consumer
  I want to manage users
  So that I can perform CRUD operations

  Scenario: Create a new user
    Given the API is running
    When I send a POST request to "/api/v1/users" with:
      | name     | email              |
      | John Doe | john@example.com   |
    Then the response status code should be 201
    And the response should contain a user ID
    And the user should be stored in the database
```

### End-to-End Integration Testing

The scaffold includes comprehensive E2E test examples:

**Database Integration** (`features/integration_db.feature`):
- Complete CRUD workflows with database persistence
- Bulk data operations
- Transaction integrity verification
- Data retrieval and filtering

**Redis Integration** (`features/integration_redis.feature`):
- Caching workflows
- Cache expiration testing
- Rate limiting scenarios
- Redis data structure usage

**Celery Integration** (`features/integration_celery.feature`):
- Background task processing
- Task failure and retry handling
- Concurrent task execution
- Task result verification

### Step Definitions

Step definitions connect Gherkin steps to Python code:

```python
from behave import given, when, then
from httpx import AsyncClient

@given('the API is running')
async def step_api_running(context):
    context.client = AsyncClient(base_url="http://localhost:8000")

@when('I send a POST request to "{endpoint}" with')
async def step_post_request(context, endpoint):
    data = {row['name']: row['email'] for row in context.table}
    context.response = await context.client.post(endpoint, json=data)

@then('the response status code should be {status_code:d}')
def step_check_status(context, status_code):
    assert context.response.status_code == status_code
```

## Celery Task Patterns

### Task Definition

```python
from app.core.celery_app import celery_app
from app.core.config import settings

@celery_app.task(bind=True, max_retries=3)
def send_email(self, recipient: str, subject: str, body: str):
    try:
        # Email sending logic
        return {"status": "sent", "recipient": recipient}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

### Task Invocation

```python
# Async (non-blocking)
send_email.delay("user@example.com", "Welcome", "Hello!")

# With ETA
from datetime import datetime, timedelta
send_email.apply_async(
    args=["user@example.com", "Reminder", "Don't forget!"],
    eta=datetime.now() + timedelta(hours=1)
)
```

## Pre-commit Configuration

The scaffold includes comprehensive pre-commit hooks:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
```

## GitHub Actions Workflows

### CI Pipeline (`ci.yml`)

Runs on every push and pull request:
1. Lint code with ruff
2. Type check with mypy
3. Run unit tests with pytest
4. Run BDD tests with behave
5. Generate coverage report
6. Security scan with bandit

### CD Pipeline (`cd.yml`)

Runs on tags/releases:
1. Build Docker image
2. Run full test suite
3. Push to container registry
4. Deploy to staging/production

## Agent Instructions

### When Creating New Projects from This Scaffold

1. **Use cookiecutter** to generate the project:
   ```bash
   cookiecutter gh:ElCuboNegro/scaffold
   ```

2. **Initialize the environment**:
   ```bash
   cd <project_slug>
   poetry install  # or pip install -r requirements.txt
   pre-commit install
   ```

3. **Start services**:
   ```bash
   docker-compose up -d  # PostgreSQL, Redis
   alembic upgrade head  # Run migrations
   uvicorn app.main:app --reload  # Start API
   celery -A app.core.celery_app worker --loglevel=info  # Start worker
   ```

4. **Run tests**:
   ```bash
   behave  # BDD tests
   pytest  # Unit tests
   ```

### When Modifying the Scaffold

1. **Update template files** in `{{cookiecutter.project_slug}}/`
2. **Test generation** with different cookiecutter variables
3. **Update `cookiecutter.json`** if adding new variables
4. **Document changes** in both `AGENTS.md` and `README.md`
5. **Update hooks** in `hooks/post_gen_project.py` for automation

### When Adding Features

1. **API Endpoints**: Add to `app/api/v1/endpoints/`
2. **Models**: Define in `app/models/`
3. **Schemas**: Create Pydantic models in `app/schemas/`
4. **CRUD Operations**: Implement in `app/crud/`
5. **Celery Tasks**: Add to `app/tasks/`
6. **BDD Tests**: Write features in `features/` with steps in `features/steps/`
7. **Migrations**: Generate with `alembic revision --autogenerate -m "description"`

### Code Quality Standards

- **Type hints required** for all function signatures
- **Docstrings required** for public APIs (Google style)
- **Test coverage minimum**: 80%
- **All tests must pass** before committing
- **No security vulnerabilities** (bandit must pass)
- **Follow PEP 8** (enforced by ruff)

## Common Patterns

### Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.user.get(db, id=user_id)
```

### Error Handling

```python
from fastapi import HTTPException, status

@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud.user.get_by_email(db, email=user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.user.create(db, obj_in=user)
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/users")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    new_user = crud.user.create(db, obj_in=user)
    background_tasks.add_task(send_welcome_email, new_user.email)
    return new_user
```

## Environment Configuration

### Development (`.env`)

```env
# API
API_V1_STR=/api/v1
PROJECT_NAME=My API
DEBUG=true

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Production

Use environment variables or secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)

## Deployment Considerations

### Docker Production Build

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Monitoring

- **Logs**: Structured JSON logging with `structlog`
- **Metrics**: Prometheus metrics via `prometheus-fastapi-instrumentator`
- **Tracing**: OpenTelemetry for distributed tracing
- **APM**: Integration with Sentry, DataDog, or New Relic

## Best Practices for AI Agents

1. **Always run tests** after making changes
2. **Generate migrations** after model changes
3. **Update BDD features** when adding new endpoints
4. **Keep dependencies updated** but test thoroughly
5. **Document API changes** in OpenAPI/Swagger
6. **Use type hints** for better IDE support and error detection
7. **Write descriptive commit messages** following Conventional Commits
8. **Review security implications** of all changes
9. **Optimize database queries** (use `select_in_load` for relationships)
10. **Handle errors gracefully** with proper HTTP status codes

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Behave Documentation](https://behave.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Support

For issues, questions, or contributions:
- **GitHub Issues**: [ElCuboNegro/scaffold/issues](https://github.com/ElCuboNegro/scaffold/issues)
- **Discussions**: [ElCuboNegro/scaffold/discussions](https://github.com/ElCuboNegro/scaffold/discussions)

---

**Last Updated**: 2025-11-25  
**Scaffold Version**: 1.0.0  
**Maintainer**: Juan Jose Alban Ortiz
