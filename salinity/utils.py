from functools import reduce
from typing import Iterable

import salt.utils.dictupdate


def merge(*items: dict) -> dict:
    return reduce(salt.utils.dictupdate.update, items)
