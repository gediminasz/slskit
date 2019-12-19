import salt.output
import salt.pillar

from salinity.mocks import MockDict, MockVault, PrettyMock
from salinity.opts import build_opts
from salinity.renderer import Renderer
from salinity.top import Minion, Top


def items(args):
    opts = build_opts(args)

    result = {
        minion_id: compile_pillar(opts, {}, minion_id) for minion_id in args.minion_id
    }

    salt.output.display_output(result, out="yaml", opts=opts)


def compile_pillar(opts, grains, minion_id):
    return salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()


def top(args) -> dict:
    return _load_top(args).top()


def _load_top(args) -> Top:
    context = {"salt": MockDict(vault=MockVault()), "grains": PrettyMock(name="GRAIN")}
    renderer = Renderer(args.pillar_root, context)
    return Top.load(args.pillar_root, args.pillar_top, renderer)
