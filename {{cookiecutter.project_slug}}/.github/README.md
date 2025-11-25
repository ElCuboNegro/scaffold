# GitHub Templates

This directory contains templates to help maintain consistency and quality in contributions to this project.

## Available Templates

### Issue Templates

We provide structured issue templates to help you report bugs, request features, or suggest documentation improvements:

- **Bug Report** - Report API bugs or issues
- **Feature Request** - Suggest new API features or enhancements
- **Documentation** - Report documentation issues or improvements

When creating a new issue, GitHub will prompt you to select the appropriate template.

### Pull Request Template

When you create a pull request, a template will automatically populate with sections for:
- Description and motivation
- Type of change
- API changes (new/modified/deprecated endpoints)
- Database migrations
- Testing performed (unit, integration, BDD)
- Performance and security considerations
- Deployment notes

Please fill out all relevant sections to help maintainers review your contribution.

### Commit Message Template

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

#### Setup

Configure your local repository to use the commit template:

```bash
git config commit.template .github/COMMIT_TEMPLATE.txt
```

#### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Test changes
- `chore` - Build process or auxiliary tool changes
- `perf` - Performance improvements
- `ci` - CI/CD changes
- `build` - Build system or dependency changes
- `migrate` - Database migrations
- `revert` - Revert a previous commit

#### Common Scopes

- `api` - API endpoints
- `auth` - Authentication/authorization
- `users` - User management
- `database` - Database operations
- `cache` - Caching layer
- `models` - Database models
- `schemas` - Pydantic schemas
- `tests` - Test files
- `docs` - Documentation

#### Examples

```
feat(auth): add JWT token refresh endpoint

Implement token refresh mechanism to allow users to obtain
new access tokens without re-authenticating.

Fixes #42
```

```
fix(database): resolve connection pool exhaustion

Increase max pool size from 10 to 50 and add connection
recycling to prevent pool exhaustion under high load.

Fixes #128
```

```
migrate(users): add email verification column

Add is_email_verified boolean column to users table
to support email verification feature.

Related to #156
```

## Contributing

For detailed contribution guidelines, please see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Questions?

If you have questions or want to discuss ideas, please use [GitHub Discussions](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}/discussions).
