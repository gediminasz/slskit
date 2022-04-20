import logging
from typing import Any, Iterable

import colorlog

LEVEL_CHOICES = tuple(logging._nameToLevel.keys())


def basic_config(**kwargs: Any) -> None:
    # borrowed `force` implementation from Python 3.8
    # https://github.com/python/cpython/blob/v3.8.0/Lib/logging/__init__.py#L1954-L1958
    # TODO use basicConfig(..., force=True) after dropping support for Python 3.7
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()

    colorlog.basicConfig(**kwargs)


def log_errors(title: str, errors: Iterable[str]) -> None:
    logging.error("\n    ".join((title, *errors)))
