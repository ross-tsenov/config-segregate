# README for Python Project Template

This Python Project Template is designed to streamline the development process, focusing on best practices, code quality, and documentation. It employs a variety of tooling and a structured folder layout to ensure maintainability and ease of use. Below is an overview of its key components, tooling, folder structure, and useful commands to get you started.

## Tooling

- [**Poetry**](https://github.com/python-poetry/poetry): Used for dependency management and packaging, making it simple to manage project libraries and their versions.
- [**Pydantic Settings**](https://github.com/pydantic/pydantic-settings): Loads and validates settings from `.env` files, ensuring configurations are both accessible and correctly typed.
- [**Ruff**](https://github.com/astral-sh/ruff): A fast and comprehensive linter that checks for syntax errors and enforces style consistency.
- [**Mypy**](https://github.com/python/mypy): A static type checker for Python, enhancing code quality and detect errors before runtime.
- [**Pytest**](https://github.com/pytest-dev/pytest): The go-to framework for writing and running tests, ensuring your code behaves as expected.
- [**Pre-commit**](https://github.com/pre-commit/pre-commit): Runs a series of checks (linting, formatting, type checking) before each commit to maintain code quality.
- [**MkDocs**](https://github.com/mkdocs/mkdocs): Generates project documentation from Markdown files, making it easy to create and maintain up-to-date documentation.
- [**Simple Logger**](https://docs.python.org/3/library/logging.html): A basic logging implementation that can be easily customized and integrated throughout the project.
- [**Devcontainer**](https://github.com/microsoft/vscode-dev-containers): Supports development inside a Docker container in VSCode or GitHub Codespaces, providing a consistent and isolated development environment.
- [**GitHub Actions**](https://github.com/features/actions): Automates linting, type checking, and testing workflows, ensuring that code meets quality standards before merging.

## Folder Structure

- `.devcontainer/`: Contains Docker configurations for the development environment, including a `Dockerfile` and `devcontainer.json` for container settings.
- `.github/workflows/`: Stores CI configurations for automated linting, typing, and testing. It's extendable for additional workflows.
- `docs/`: Holds MkDocs structured documentation, serving as the home for project documentation.
  - `docs/assets/`: Stores images and other assets for the documentation.
- `scripts/`: Typically includes utility bash scripts.
- `src/`: The primary directory for project source code.
  - `src/settings.py`: Manages application settings loaded and validated from `.env`.
  - `src/logger.py`: Provides a global logger accessible throughout the project.
- `tests/`: Contains test cases and fixtures for the project.
  - `tests/conftest.py`: Defines reusable pytest fixtures.
  - `tests/core.py`: Tests core functionalities like settings and logging.
- `.env.sample`: An example `.env` file outlining required environment variables.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `.pre-commit-config.yaml`: Configures checks to run before commits.
- `main.py`: The entry point for running the application.
- `mkdocs.yml`: Configuration for MkDocs.
- `pyproject.toml`: Specifies project settings, dependencies, and build information.

Sure, here are the useful commands with code blocks for better readability:

### Useful Commands

- **Poetry Commands**

  Install dependencies:
  ```bash
  poetry install [--with dev] [--with docs]
  ```


- **Pre-commit Commands**

  Install pre-commit hooks:
  ```bash
  pre-commit install
  ```
  Run all pre-commit hooks:
  ```bash
  pre-commit run --all-files
  ```

- **Mypy Commands**

  Run type checking:
  ```bash
  mypy src/ tests/
  ```

- **Pytest Commands**

  Run tests:
  ```bash
  pytest tests
  ```

- **MkDocs Commands**

  Serve documentation locally:
  ```bash
  mkdocs serve
  ```
  Build static site:
  ```bash
  mkdocs build
  ```

- **Devcontainer Command**

  To use the devcontainer, if you are using VSCode, follow these steps:
  - Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
  - Type and select "Remote-Containers: Open Folder in Container".

  Alternatively, if you are using GitHub Codespaces, it will automatically use the `.devcontainer` configuration when you create a new codespace.

This project template is equipped with a robust set of tools and a clear structure to help you start your Python project on the right foot. Adjust and extend it as needed to fit your project requirements.
