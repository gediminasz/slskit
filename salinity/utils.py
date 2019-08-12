from functools import reduce

import yaml

import salt.utils.dictupdate


def merge(*items: dict) -> dict:
    return reduce(salt.utils.dictupdate.update, items)


def pretty_print(structure: dict):
    print(yaml.dump(structure))
