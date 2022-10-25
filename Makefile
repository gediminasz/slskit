check:
	poetry run black --check .
	poetry run pylint slskit tests
	poetry run mypy --strict --allow-untyped-decorators

	poetry run slskit refresh
	poetry run slskit highstate | diff highstate.snap -

	poetry run pytest

snapshot:
	poetry run pytest --snapshot-update
	poetry run slskit highstate > highstate.snap

update:
	poetry add "salt>=3004.0"
	poetry add click@latest colorlog@latest funcy@latest jsonschema@latest
	poetry add --group=dev black@latest GitPython@latest mypy@latest pylint@latest pytest@latest pytest-snapshot@latest types-PyYAML@latest
	poetry lock

publish:
	poetry publish -v --build
