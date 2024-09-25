all: lint test

install:
	poetry install

lint:
	poetry run black --check .
	poetry run mypy --strict --allow-untyped-decorators

test:
	poetry run slskit refresh
	poetry run pytest

snapshots:
	poetry run pytest --snapshot-update

update:
	poetry add "salt>=3006.0"
	poetry add click@latest colorlog@latest funcy@latest jsonschema@latest
	poetry lock

publish:
	rm -rfv ./dist
	poetry publish -v --build
