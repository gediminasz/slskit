from pathlib import Path

import yaml

from salinity.renderer import Renderer
from salinity.utils import merge


class Top:
    @staticmethod
    def load(
        root: str, top: str, renderer: Renderer, environment: str = "base"
    ) -> "Top":
        definition = yaml.safe_load((Path(root) / top).read_text())
        body = {
            selector: merge(*map(renderer.render, names))
            for selector, names in definition[environment].items()
        }
        return Top(body)

    def __init__(self, body: dict):
        self.body = body

    def for_minion(self, minion_id: str) -> dict:
        result: dict = {}
        for selector, data in self.body.items():
            if self._matches(minion_id, selector):
                result.update(data)
        return result

    def _matches(self, minion_id: str, selector: str) -> bool:
        return (selector == "*") or (minion_id in selector)
