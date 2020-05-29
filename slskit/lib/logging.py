import logging
from typing import Any

import colorlog

LEVEL_CHOICES = logging._nameToLevel.keys()  # noqa


def basic_config(**kwargs: Any) -> None:
    # borrowed `force` implementation from Python 3.8
    # https://github.com/python/cpython/blob/v3.8.0/Lib/logging/__init__.py#L1954-L1958
    # TODO use basicConfig(..., force=True) after dropping support for Python 3.7
    for h in logging.root.handlers[:]:
        logging.root.removeHandler(h)
        h.close()

    colorlog.basicConfig(**kwargs)
