from pprint import pprint
from pathlib import Path
import os

import yaml

def matches(minion_id, selector):
    return (selector == "*") or (minion_id in selector)

def load_pillar(root_path, pillar_id):
    path = root_path.joinpath(*pillar_id.split("."))
    if path.with_suffix(".sls").exists():
        return load_yaml(path.with_suffix(".sls"))
    return load_yaml(path / "init.sls")

def load_yaml(path):
    with path.open() as f:
        return yaml.safe_load(f)

root_path = Path("pillar")
top_file = root_path / "top.sls"

minions = {
    "stuart": {},
    "kevin": {},
    "bob": {},
}

for selector, pillars in load_yaml(top_file)["base"].items():
    for pillar_id in pillars:
        data = load_pillar(root_path, pillar_id)

        for minion_id, minion_data in minions.items():
            if matches(minion_id, selector):
                minion_data.update(data)

pprint(minions)
