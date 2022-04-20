import tomli

import slskit


def test_version_in_module_matches_pyproject():
    with open("pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
    assert slskit.__version__ == pyproject["tool"]["poetry"]["version"]
