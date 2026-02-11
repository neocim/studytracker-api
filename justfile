lint:
    ruff format
    ruff check --fix
    mypy
    lint-imports
    typos