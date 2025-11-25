# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup from cookiecutter template
- FastAPI application with example endpoints
- Celery task queue integration
- BDD testing with Behave
- Unit testing with pytest
{% if cookiecutter.use_postgresql == "yes" -%}
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations
{% endif -%}
{% if cookiecutter.use_redis == "yes" -%}
- Redis for caching and message broker
{% endif -%}
{% if cookiecutter.include_auth == "yes" -%}
- JWT authentication system
{% endif -%}
{% if cookiecutter.use_docker == "yes" -%}
- Docker and Docker Compose configuration
{% endif -%}
- Pre-commit hooks for code quality
- GitHub Actions CI/CD pipeline
- Architecture validation with import-linter

## [{{ cookiecutter.version }}] - {% now 'utc', '%Y-%m-%d' %}

### Added
- Initial release

[Unreleased]: https://github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.project_slug }}/compare/v{{ cookiecutter.version }}...HEAD
[{{ cookiecutter.version }}]: https://github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.project_slug }}/releases/tag/v{{ cookiecutter.version }}
