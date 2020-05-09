import runpy

PACKAGE_NAME = "slskit"


def run_module() -> None:
    runpy.run_module(PACKAGE_NAME)
