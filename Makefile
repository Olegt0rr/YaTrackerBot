.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

format:
	ruff format app tools tests

mypy:
	mypy -p app

ruff:
	ruff check app --fix
	ruff check tools --fix
	ruff check tests --fix

lint: ruff mypy format


run:
	uv run python -m app
