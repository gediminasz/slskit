import toml

import slskit


def test_version_in_module_matches_pyproject():
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)
    assert slskit.__version__ == pyproject["tool"]["poetry"]["version"]
