from argparse import ArgumentParser

import salinity.pillar
import salinity.state
from salinity.utils import pretty_print


def command(function):
    return lambda args: pretty_print(function(args))


parser = ArgumentParser(prog="salinity", description="Salinity - Salt testing toolkit.")
parser.add_argument(
    "--state-root", default="salt", help="path to state root directory (default: salt)"
)
parser.add_argument(
    "--state-top", default="top.sls", help="state top file name (default: top.sls)"
)
parser.add_argument(
    "--pillar-root",
    default="pillar",
    help="path to pillar root directory (default: pillar)",
)
parser.add_argument(
    "--pillar-top", default="top.sls", help="pillar top file name (default: top.sls)"
)
subparsers = parser.add_subparsers(title="commands")


parser_state_show = subparsers.add_parser(
    "state.show", help="renders the states for the specified minions"
)
parser_state_show.add_argument("minion_id", nargs="+")
parser_state_show.set_defaults(func=command(salinity.state.show))


parser_state_show_highstate = subparsers.add_parser(
    "state.show_highstate", help="renders the states for the specified minions"
)
parser_state_show_highstate.add_argument("minion_id", nargs="+")
parser_state_show_highstate.set_defaults(func=salinity.state.show_highstate)


parser_pillar_top = subparsers.add_parser(
    "pillar.top", help="renders the pillar top file"
)
parser_pillar_top.set_defaults(func=command(salinity.pillar.top))


parser_pillar_items = subparsers.add_parser(
    "pillar.items", help="renders pillar items for the specified minions"
)
parser_pillar_items.add_argument("minion_id", nargs="+")
parser_pillar_items.set_defaults(func=salinity.pillar.items)


args = parser.parse_args()
if "func" in args:
    args.func(args)
else:
    parser.print_usage()
