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

        blocks = [
            Block(selector, names, renderer)
            for selector, names in definition[environment].items()
        ]

        return Top(blocks)

    def __init__(self, blocks: list):
        self.blocks = blocks

    def for_minion(self, minion) -> dict:
        print(minion)
        result: dict = {}
        for block in self.blocks:
            if block.matches(minion):
                result.update(block.render())
        return result


class Block:
    def __init__(self, selector: str, names: list, renderer: Renderer):
        self.selector = selector

        if isinstance(names[0], dict):
            self.match_by = names[0]["match"]
            self.names = names[1:]
        else:
            self.match_by = "glob"
            self.names = names

        self.renderer = renderer

    def matches(self, minion) -> bool:
        if self.match_by == "glob":
            # TODO proper glob matching
            return (self.selector == "*") or (minion.mid in self.selector)
        elif self.match_by == "pillar":
            # TODO proper pillar matching
            return False
        return False

    def render(self):
        return merge(*map(self.renderer.render, self.names))


class Minion:
    def __init__(self, mid, pillar=None):
        self.mid = mid
        self.pillar = pillar
