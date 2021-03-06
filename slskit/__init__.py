import runpy

__version__ = VERSION = "2021.3.0"

PACKAGE_NAME = "slskit"


def run_module() -> None:
    runpy.run_module(PACKAGE_NAME)
