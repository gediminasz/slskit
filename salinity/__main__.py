import os
from pathlib import Path
from pprint import pprint
from unittest.mock import MagicMock

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from salt.utils.decorators.jinja import JinjaFilter
from salt.utils.jinja import SerializerExtension

root_path = Path("pillar")
jinja_env = Environment(
    loader=FileSystemLoader(str(root_path)), extensions=[SerializerExtension]
)
jinja_env.filters.update(JinjaFilter.salt_jinja_filters)


def matches(minion_id, selector):
    return (selector == "*") or (minion_id in selector)


def load_pillar(pillar_id):
    path = Path(*pillar_id.split("."))
    if root_path.joinpath(path).with_suffix(".sls").exists():
        return render_yaml(path.with_suffix(".sls"))
    return render_yaml(path / "init.sls")


def render_yaml(path: Path) -> str:
    template = jinja_env.get_template(str(path.as_posix()))
    content = template.render(salt=MagicMock(name="salt"))
    return yaml.safe_load(content)


top_file = Path("top.sls")

minions = {"stuart": {}, "kevin": {}, "bob": {}}

for selector, pillars in render_yaml(top_file)["base"].items():
    for pillar_id in pillars:
        data = load_pillar(pillar_id)

        for minion_id, minion_data in minions.items():
            if matches(minion_id, selector):
                minion_data.update(data)

print(yaml.dump(minions, sort_keys=False))

# TODO PILLAR NAMESPACE FLATTENING
# TODO PILLAR DICTIONARY MERGING
# TODO INCLUDING OTHER PILLARS
# https://docs.saltstack.com/en/latest/topics/pillar/#declaring-the-master-pillar
