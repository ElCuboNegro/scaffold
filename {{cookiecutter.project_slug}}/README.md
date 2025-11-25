# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- ✨ **FastAPI** - Modern, fast web framework with automatic API documentation
- 🔄 **Celery** - Distributed task queue for background jobs
- 🧪 **BDD Testing** - Behavior-Driven Development with Behave
- 🐳 **Docker** - Containerized development and production environments
{% if cookiecutter.use_postgresql == "yes" -%}
- 🗄️ **PostgreSQL** - Production-ready relational database
{% endif -%}
{% if cookiecutter.use_redis == "yes" -%}
- 🚀 **Redis** - High-performance caching and message broker
{% endif -%}
{% if cookiecutter.include_auth == "yes" -%}
- 🔐 **Authentication** - JWT-based authentication system
{% endif -%}
- ✅ **Pre-commit Hooks** - Automated code quality checks
- 🔄 **GitHub Actions** - CI/CD pipelines
- 📝 **Alembic** - Database migration management

## Quick Start

### Prerequisites

- Python {{ cookiecutter.python_version }}
- Poetry (recommended) or pip
{% if cookiecutter.use_docker == "yes" -%}
- Docker and Docker Compose
{% endif -%}
{% if cookiecutter.use_postgresql == "yes" and cookiecutter.use_docker == "no" -%}
- PostgreSQL
{% endif -%}
{% if cookiecutter.use_redis == "yes" and cookiecutter.use_docker == "no" -%}
- Redis
{% endif %}

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd {{ cookiecutter.project_slug }}
   ```

2. **Install dependencies**:
   ```bash
   # Using Poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

{% if cookiecutter.use_docker == "yes" -%}
5. **Start services with Docker**:
   ```bash
   docker-compose up -d
   ```
{% else -%}
5. **Start required services**:
{% if cookiecutter.use_postgresql == "yes" -%}
   - Start PostgreSQL
{% endif -%}
{% if cookiecutter.use_redis == "yes" -%}
   - Start Redis
{% endif %}
{% endif %}

6. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Start Celery worker** (in a separate terminal):
   ```bash
   celery -A app.core.celery_app worker --loglevel=info
   ```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

### Run BDD Tests (Behave)

```bash
behave
```

### Run Unit Tests (pytest)

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run All Quality Checks

```bash
# Linting
ruff check .

# Type checking
mypy app

# Security scan
bandit -r app

# Format check
ruff format --check .
```

## Development

### Project Structure

```
{{ cookiecutter.project_slug }}/
├── app/                    # Application code
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── crud/              # CRUD operations
│   ├── tasks/             # Celery tasks
│   └── main.py            # Application entry point
├── features/              # BDD test features
├── tests/                 # Unit/integration tests
├── alembic/               # Database migrations
├── docker/                # Docker configurations
└── .github/               # GitHub Actions workflows
```

### Creating a New Endpoint

1. Define the schema in `app/schemas/`
2. Create the model in `app/models/`
3. Implement CRUD operations in `app/crud/`
4. Add the endpoint in `app/api/v1/endpoints/`
5. Register the router in `app/api/v1/router.py`
6. Write BDD tests in `features/`

### Creating a Database Migration

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Creating a Celery Task

```python
from app.core.celery_app import celery_app

@celery_app.task
def my_background_task(param: str):
    # Task logic here
    return {"result": "success"}
```

## Deployment

{% if cookiecutter.use_docker == "yes" -%}
### Docker Production Build

```bash
docker build -t {{ cookiecutter.project_slug }}:latest .
docker run -p 8000:8000 {{ cookiecutter.project_slug }}:latest
```

### Docker Compose Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```
{% endif %}

### Environment Variables

See `.env.example` for all available configuration options.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the {{ cookiecutter.license }} License - see the LICENSE file for details.

## Author

**{{ cookiecutter.author_name }}** - [{{ cookiecutter.author_email }}](mailto:{{ cookiecutter.author_email }})

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Task queue powered by [Celery](https://docs.celeryproject.org/)
- BDD testing with [Behave](https://behave.readthedocs.io/)
