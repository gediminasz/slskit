import sys

import yaml

from salinity.top import Top


def pretty_print(structure: dict):
    print(yaml.dump(structure, sort_keys=False))  # type: ignore


if __name__ == "__main__":
    top = Top.load("pillar")

    if len(sys.argv) == 1:
        pretty_print(top.body)
    else:
        result = {minion_id: top.for_minion(minion_id) for minion_id in sys.argv[1:]}
        pretty_print(result)
