from pathlib import Path

from salinity.render import render_pillar, template_exists


class PillarTop:
    def __init__(self, path: str = "top.sls", environment: str = "base"):
        self.path: Path = Path(path)
        self.environment: str = environment
        self.top: dict = render_pillar(self.path)[environment]
        self.pillars: dict = self._load_pillars()

    def for_minion(self, minion_id: str) -> dict:
        result: dict = {}
        for selector, pillars in self.pillars.items():
            if self._matches(minion_id, selector):
                for pillar in pillars:
                    result.update(pillar)
        return result

    def _matches(self, minion_id: str, selector: str) -> bool:
        return (selector == "*") or (minion_id in selector)

    def _load_pillars(self) -> dict:
        return {
            selector: [self._load_single(pillar_name) for pillar_name in pillar_names]
            for selector, pillar_names in self.top.items()
        }

    def _load_single(self, pillar_name: str) -> dict:
        return render_pillar(self._resolve_path(pillar_name))

    def _resolve_path(self, pillar_name: str) -> Path:
        path = Path(*pillar_name.split("."))
        sls_path = path.with_suffix(".sls")
        return sls_path if template_exists(sls_path) else path / "init.sls"
