from pathlib import Path
from unittest.mock import MagicMock

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from salt.utils.decorators.jinja import JinjaFilter
from salt.utils.jinja import SerializerExtension


class Renderer:
    def __init__(self, root: str):
        self.jinja_env = Environment(
            loader=FileSystemLoader(root), extensions=[SerializerExtension]
        )
        self.jinja_env.filters.update(JinjaFilter.salt_jinja_filters)

    def render(self, name: str) -> dict:
        path = self.resolve_path(name)
        template = self.jinja_env.get_template(str(path))

        # TODO GZL refactor
        mock_salt = MagicMock(name="salt")
        mock_salt["vault"].read_secret = self._read_secret

        content = template.render(salt=mock_salt, grains=MagicMock(name="grains"))
        return yaml.safe_load(content)

    def _read_secret(self, path, key=None):
        if not key:
            return {"SECRET": {"path": path}}
        return f"SECRET {path} {key}"

    def resolve_path(self, name: str) -> Path:
        path = Path(*name.split("."))
        sls_path = path.with_suffix(".sls")
        return sls_path if self.template_exists(sls_path) else path / "init.sls"

    def template_exists(self, path: Path) -> bool:
        return str(path) in self.jinja_env.list_templates()
