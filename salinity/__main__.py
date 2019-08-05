from pprint import pprint
from pathlib import Path
import os

import yaml

root_path = Path("pillar")
top_file = root_path / "top.sls"

with top_file.open() as f:
    top = yaml.safe_load(f)

def matches(minion_id, selector):
    return (selector == "*") or (minion_id in selector)

minions = {
    "stuart": {},
    "kevin": {},
    "bob": {},
}

for selector, pillars in top["base"].items():
    for pillar in pillars:
        with (root_path / pillar).with_suffix(".sls").open() as f:
            data = yaml.safe_load(f)

    for minion_id, minion_data in minions.items():
        if matches(minion_id, selector):
            minion_data.update(data)

pprint(minions)
