import warnings
from collections import defaultdict
from pathlib import Path
from typing import Optional, Union
from unittest.mock import MagicMock

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
from salt.utils.decorators.jinja import JinjaFilter
from salt.utils.jinja import SerializerExtension, tojson


class Renderer:
    def __init__(self, root: str, context: dict):
        self.jinja_env = Environment(
            loader=FileSystemLoader(root), extensions=[SerializerExtension]
        )
        self.jinja_env.filters.update(JinjaFilter.salt_jinja_filters)
        self.jinja_env.filters.update(tojson=custom_tojson)
        self.context = context

    def render(self, name: str) -> Optional[dict]:
        try:
            path = self.resolve_path(name)
            template = self.jinja_env.get_template(str(path))

            content = template.render(self.context)
            return yaml.safe_load(content)
        except TemplateNotFound:
            warnings.warn(f"Template for '{name}' not found")

    def resolve_path(self, name: str) -> Path:
        path = Path(*name.split("."))
        sls_path = path.with_suffix(".sls")
        return sls_path if self.template_exists(sls_path) else path / "init.sls"

    def template_exists(self, path: Path) -> bool:
        return str(path) in self.jinja_env.list_templates()


def custom_tojson(val, *args, **kwargs):
    if isinstance(val, MagicMock):
        return f"{val}|tojson"
    return tojson(val, *args, **kwargs)
