import logging
from typing import Iterable

LEVEL_CHOICES = tuple(logging._nameToLevel.keys())


def log_errors(title: str, errors: Iterable[str]) -> None:
    logging.error("\n    ".join((title, *errors)))
