all: lint test

install:
	poetry install

lint:
	poetry check --lock
	# Python 3.12.5 has a memory safety issue that can cause Black's AST safety checks to fail. Please upgrade to Python 3.12.6 or downgrade to Python 3.12.4
	# poetry run black --check .
	poetry run mypy --strict --allow-untyped-decorators

test:
	poetry run slskit refresh
	poetry run pytest

snapshots:
	poetry run pytest --snapshot-update

publish:
	rm -rfv ./dist
	poetry publish -v --build

lock:
	poetry lock --regenerate
