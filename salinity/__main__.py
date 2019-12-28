from argparse import ArgumentParser

import salinity.pillar
import salinity.state
from salinity.opts import DEFAULT_CONFIG_PATHS, Config


parser = ArgumentParser(prog="salinity", description="Salinity - Salt testing toolkit.")
parser.add_argument(
    "-c",
    "--config",
    help=f"path to Salinity configuration file (default: {' or '.join(DEFAULT_CONFIG_PATHS)})",
)
subparsers = parser.add_subparsers(title="commands")

parser_state_show_highstate = subparsers.add_parser(
    "state.show_highstate", help="renders the states for the specified minions"
)
parser_state_show_highstate.add_argument("minion_id", nargs="*")
parser_state_show_highstate.set_defaults(func=salinity.state.show_highstate)

parser_pillar_items = subparsers.add_parser(
    "pillar.items", help="renders pillar items for the specified minions"
)
parser_pillar_items.add_argument("minion_id", nargs="*")
parser_pillar_items.set_defaults(func=salinity.pillar.items)


args = parser.parse_args()
config = Config(args)
if "func" in args:
    args.func(config)
else:
    parser.print_usage()
