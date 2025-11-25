"""Post-generation hook for cookiecutter."""

import os
import subprocess
import sys

# Fix encoding issues on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def run_command(command: list[str]) -> None:
    """Run a shell command."""
    try:
        subprocess.run(command, check=True)
        print(f"✓ Successfully ran: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to run: {' '.join(command)}")
        print(f"  Error: {e}")


def main() -> None:
    """Post-generation setup."""
    print("\n🚀 Setting up your project...\n")

    # Initialize git repository if not already initialized
    if not os.path.exists(".git"):
        print("📦 Initializing git repository...")
        run_command(["git", "init"])
        run_command(["git", "add", "."])
        run_command(["git", "commit", "-m", "Initial commit from cookiecutter template"])

    # Install pre-commit hooks
    print("\n🔧 Installing pre-commit hooks...")
    try:
        run_command(["pre-commit", "install"])
    except Exception:
        print("⚠️  Could not install pre-commit hooks. Run 'pre-commit install' manually.")

    {% if cookiecutter.use_postgresql == "yes" -%}
    # Create initial Alembic migration
    print("\n📝 Creating initial database migration...")
    try:
        run_command(["alembic", "revision", "--autogenerate", "-m", "Initial migration"])
    except Exception:
        print("⚠️  Could not create initial migration. Run 'alembic revision --autogenerate -m \"Initial migration\"' manually.")
    {% endif %}

    print("\n✨ Project setup complete!\n")
    print("Next steps:")
    print("  1. cd {{ cookiecutter.project_slug }}")
    print("  2. poetry install  (or pip install -r requirements.txt)")
    {% if cookiecutter.use_docker == "yes" -%}
    print("  3. docker-compose up -d")
    {% endif -%}
    {% if cookiecutter.use_postgresql == "yes" -%}
    print("  4. alembic upgrade head")
    {% endif -%}
    print("  5. uvicorn app.main:app --reload")
    print("\n📚 Documentation: http://localhost:8000/docs")
    print("🎉 Happy coding!\n")


if __name__ == "__main__":
    main()
