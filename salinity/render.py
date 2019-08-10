from unittest.mock import MagicMock

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from salt.utils.jinja import SerializerExtension

root_path = Path("pillar")
jinja_env = Environment(
    loader=FileSystemLoader(str(root_path)), extensions=[SerializerExtension]
)


def template_exists(path: Path) -> bool:
    return str(path) in jinja_env.list_templates()


def render_pillar(path: Path) -> dict:
    template = jinja_env.get_template(str(path))
    content = template.render(salt=MagicMock(name="salt"))
    return yaml.safe_load(content)
