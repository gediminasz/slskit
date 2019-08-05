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

def load_pillar(pillar_id):
    path = root_path.joinpath(*pillar_id.split(".")).with_suffix(".sls")
    with path.open() as f:
        return yaml.safe_load(f)

minions = {
    "stuart": {},
    "kevin": {},
    "bob": {},
}

for selector, pillars in top["base"].items():
    for pillar_id in pillars:
        data = load_pillar(pillar_id)

        for minion_id, minion_data in minions.items():
            if matches(minion_id, selector):
                minion_data.update(data)

pprint(minions)
