from functools import reduce, wraps

import salt.output
import salt.utils.dictupdate
import yaml


def merge(*items: dict) -> dict:
    items = filter(None, items)
    return reduce(salt.utils.dictupdate.update, items, {})


def pretty_print(structure: dict):
    print(yaml.dump(structure))
