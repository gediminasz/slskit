from salinity.mocks import MockDict
from salinity.renderer import Renderer
from salinity.top import Top


def top(args):
    context = {"pillar": MockDict(), "salt": MockDict()}
    renderer = Renderer(args.state_root, context)
    top = Top.load(args.state_root, args.state_top, renderer)
    return top.body
