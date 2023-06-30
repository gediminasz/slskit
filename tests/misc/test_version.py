try:
    import tomllib
except ImportError:  # TODO remove this workaround when Python 3.10 support is dropped
    import tomli as tomllib

import slskit


def test_version_in_module_matches_pyproject():
    with open("pyproject.toml", "rb") as project_file:
        project = tomllib.load(project_file)
    assert slskit.__version__ == project["tool"]["poetry"]["version"]
