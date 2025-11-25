# {{ cookiecutter.project_name }} - Cookiecutter Scaffold

A production-ready cookiecutter template for building BDD-tested REST APIs with FastAPI, Celery, and modern Python tooling.

## Features

- 🚀 **FastAPI** - Modern, fast web framework with automatic OpenAPI documentation
- 🔄 **Celery** - Distributed task queue for background jobs
- 🧪 **BDD Testing** - Behavior-Driven Development with Behave
- ✅ **Pre-commit Hooks** - Automated code quality checks
- 🐳 **Docker Support** - Containerized development and production
- 📊 **GitHub Actions** - CI/CD pipelines
- 🗄️ **PostgreSQL** - Production database (optional)
- 🚀 **Redis** - Caching and message broker (optional)
- 🔐 **JWT Authentication** - Token-based auth (optional)

## Quick Start

### Prerequisites

- Python 3.10+
- [Cookiecutter](https://cookiecutter.readthedocs.io/)
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Generate a New Project

```bash
# Install cookiecutter if you haven't already
pip install cookiecutter

# Generate a new project from this template
cookiecutter gh:ElCuboNegro/scaffold

# Or from a local clone
cookiecutter /path/to/scaffold
```

You'll be prompted for:
- **project_name**: Your project name (e.g., "My API Project")
- **project_slug**: Python package name (auto-generated from project_name)
- **project_description**: Brief description
- **author_name**: Your name
- **author_email**: Your email
- **python_version**: Python version (3.11, 3.10, or 3.12)
- **use_docker**: Include Docker configuration (yes/no)
- **use_postgresql**: Include PostgreSQL (yes/no)
- **use_redis**: Include Redis (yes/no)
- **include_auth**: Include JWT authentication (yes/no)
- **license**: License type (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, Proprietary)

### After Generation

```bash
cd <project_slug>

# Install dependencies
poetry install

# Install pre-commit hooks
pre-commit install

# Start services (if using Docker)
docker-compose up -d

# Run database migrations (if using PostgreSQL)
alembic upgrade head

# Start the API
uvicorn app.main:app --reload

# Start Celery worker (in another terminal)
celery -A app.core.celery_app worker --loglevel=info
```

Visit http://localhost:8000/docs for interactive API documentation.

## Project Structure

```
<project_slug>/
├── app/                    # Application code
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   │       ├── endpoints/ # Individual endpoint modules
│   │       └── router.py  # Router aggregation
│   ├── core/              # Core configuration
│   │   ├── config.py      # Settings
│   │   ├── database.py    # Database setup
│   │   ├── security.py    # Auth utilities
│   │   └── celery_app.py  # Celery config
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── crud/              # CRUD operations
│   ├── tasks/             # Celery tasks
│   └── main.py            # FastAPI app
├── features/              # BDD test features
│   ├── steps/            # Step definitions
│   └── environment.py    # Behave configuration
├── tests/                 # Unit/integration tests
├── alembic/               # Database migrations
├── .github/workflows/     # CI/CD pipelines
├── docker-compose.yml     # Docker services
├── Dockerfile             # Container image
├── pyproject.toml         # Dependencies & config
└── .pre-commit-config.yaml # Code quality hooks
```

## Development Workflow

### Running Tests

```bash
# BDD tests
behave

# Unit tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# All quality checks
pre-commit run --all-files
```

### Creating New Endpoints

1. Define schema in `app/schemas/`
2. Create model in `app/models/` (if using database)
3. Implement CRUD in `app/crud/`
4. Add endpoint in `app/api/v1/endpoints/`
5. Register router in `app/api/v1/router.py`
6. Write BDD tests in `features/`

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Technology Stack

- **Web Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Task Queue**: Celery
- **Database**: PostgreSQL + SQLAlchemy
- **Cache/Broker**: Redis
- **Testing**: Behave (BDD) + pytest
- **Linting**: Ruff
- **Type Checking**: mypy
- **Security**: Bandit
- **Containers**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## Configuration

All configuration is managed through environment variables. See `.env.example` in the generated project.

## Contributing to the Template

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different cookiecutter options
5. Submit a pull request

## License

This template is licensed under the MIT License. Generated projects can use any license selected during generation.

## Support

- **Issues**: [GitHub Issues](https://github.com/ElCuboNegro/scaffold/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ElCuboNegro/scaffold/discussions)

## Author

**Juan Jose Alban Ortiz**

---

**Happy coding! 🚀**
