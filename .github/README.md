# GitHub Templates

This directory contains templates to help maintain consistency and quality in contributions to this project.

## Available Templates

### Issue Templates

We provide structured issue templates to help you report bugs, request features, or suggest documentation improvements:

- **Bug Report** - Report issues with the scaffold template
- **Feature Request** - Suggest new features or enhancements
- **Documentation** - Report documentation issues or improvements

When creating a new issue, GitHub will prompt you to select the appropriate template.

### Pull Request Template

When you create a pull request, a template will automatically populate with sections for:
- Description and motivation
- Type of change
- Testing performed
- Quality checklist

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
- `revert` - Revert a previous commit

#### Examples

```
feat(cookiecutter): add support for custom database backends

Allow users to select from PostgreSQL, MySQL, or SQLite
when generating a new project from the template.

Fixes #42
```

```
fix(docker): resolve database connection timeout

Increase connection timeout from 5s to 30s to handle
slower network conditions during container startup.

Fixes #128
```

## Contributing

For detailed contribution guidelines, please see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Questions?

If you have questions or want to discuss ideas, please use [GitHub Discussions](https://github.com/ElCuboNegro/scaffold/discussions).
