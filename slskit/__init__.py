import runpy

__version__ = VERSION = "2020.6.0"

PACKAGE_NAME = "slskit"


def run_module() -> None:
    runpy.run_module(PACKAGE_NAME)
