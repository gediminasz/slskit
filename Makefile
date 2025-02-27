all: lint test

install:
	poetry install

lint:
	poetry check --lock
	poetry run black --check .
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
