import tomli

import slskit


def test_version_in_module_matches_pyproject():
    with open("pyproject.toml", "rb") as project_file:
        project = tomli.load(project_file)
    assert slskit.__version__ == project["tool"]["poetry"]["version"]
