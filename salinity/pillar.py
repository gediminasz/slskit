from salinity.mocks import MockDict, MockVault, PrettyMock
from salinity.renderer import Renderer
from salinity.top import Minion, Top


def top(args) -> dict:
    return _load_top(args).body


def items(args) -> dict:
    top = _load_top(args)
    return {
        minion_id: top.for_minion(Minion(minion_id)) for minion_id in args.minion_id
    }


def _load_top(args) -> Top:
    context = {"salt": MockDict(vault=MockVault()), "grains": PrettyMock(name="GRAIN")}
    renderer = Renderer(args.pillar_root, context)
    return Top.load(args.pillar_root, args.pillar_top, renderer)
