from pathlib import Path

from salinity.renderer import Renderer


class PillarTop:
    def __init__(self, root: str = "pillar", environment: str = "base"):
        self.root = Path(root)
        self.environment = environment

        self.renderer = Renderer(root)
        self.top: dict = self.renderer.render("top")[environment]
        self.pillars = {
            selector: list(map(self.renderer.render, pillar_names))
            for selector, pillar_names in self.top.items()
        }

    def for_minion(self, minion_id: str) -> dict:
        result: dict = {}
        for selector, pillars in self.pillars.items():
            if self._matches(minion_id, selector):
                for pillar in pillars:
                    result.update(pillar)
        return result

    def _matches(self, minion_id: str, selector: str) -> bool:
        return (selector == "*") or (minion_id in selector)
