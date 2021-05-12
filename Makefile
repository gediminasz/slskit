check:
	poetry run black --check .
	poetry run pylint slskit tests
	poetry run mypy --strict --allow-untyped-decorators

	poetry run slskit refresh
	poetry run slskit highstate | diff highstate.snap -

	poetry run pytest

snapshot:
	poetry run slskit highstate > highstate.snap
