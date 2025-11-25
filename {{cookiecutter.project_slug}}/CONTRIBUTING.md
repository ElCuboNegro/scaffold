# Contributing to {{ cookiecutter.project_name }}

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd {{ cookiecutter.project_slug }}
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   pre-commit install
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

{% if cookiecutter.use_docker == "yes" -%}
4. **Start services**:
   ```bash
   docker-compose up -d
   ```
{% endif %}

## Development Workflow

### Creating a Feature

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Write tests for your changes:
   - Unit tests in `tests/`
   - BDD scenarios in `features/`

4. Run quality checks:
   ```bash
   # Run all pre-commit hooks
   pre-commit run --all-files
   
   # Run tests
   pytest
   behave
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. Push and create a pull request

## Coding Standards

### Code Style

- Follow PEP 8 (enforced by ruff)
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Documentation

- Add docstrings to all public functions and classes (Google style)
- Update README.md if adding new features
- Add comments for complex logic

### Testing

- Maintain minimum 80% code coverage
- Write BDD scenarios for user-facing features
- Write unit tests for business logic
- All tests must pass before merging

### Architecture

- Follow the layered architecture:
  - `api/` → `schemas/` | `crud/` → `models/` | `core/`
- No circular dependencies (enforced by import-linter)
- Keep business logic in `crud/` and `tasks/`
- API endpoints should be thin controllers

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add user authentication endpoint
fix: resolve database connection timeout
docs: update API documentation
test: add tests for user CRUD operations
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Ensure pre-commit hooks pass
5. Update CHANGELOG.md (if applicable)
6. Request review from maintainers

## Code Review Guidelines

Reviewers should check:

- [ ] Code follows project standards
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance implications considered
- [ ] Security implications considered

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Suggestions for improvements

Thank you for contributing! 🎉
