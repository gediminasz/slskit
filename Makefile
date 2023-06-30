all: lint test

lint:
	poetry run black --check .
	poetry run slskit tests
	poetry run mypy --strict --allow-untyped-decorators

test:
	poetry run slskit refresh
	poetry run slskit highstate | diff highstate.snap -
	poetry run pytest

snapshot:
	poetry run pytest --snapshot-update
	poetry run slskit highstate > highstate.snap

update:
	poetry add "salt>=3004.0"
	poetry add click@latest colorlog@latest funcy@latest jsonschema@latest
	poetry add --group=dev black@latest GitPython@latest mypy@latest pytest@latest pytest-snapshot@latest types-PyYAML@latest
	poetry lock

publish:
	rm -rfv ./dist
	poetry publish -v --build
