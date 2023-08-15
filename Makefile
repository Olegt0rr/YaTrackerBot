.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

black:
	black app/

mypy:
	mypy -p app

ruff:
	ruff check app --fix
	ruff check tools --fix
	ruff check tests --fix

lint: ruff mypy black


run:
	poetry run python -m app
