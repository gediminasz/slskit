import logging  # isort:skip
import colorlog  # isort:skip

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
)
logging.basicConfig(level=logging.WARNING, handlers=(handler,))


from argparse import ArgumentParser

from . import PACKAGE_NAME, pillar, state
from .opts import DEFAULT_CONFIG_PATHS, Config

parser = ArgumentParser(
    prog=PACKAGE_NAME,
    description=f"{PACKAGE_NAME} - tools for checking Salt state validity",
)
parser.add_argument(
    "-c",
    "--config",
    help=f"path to {PACKAGE_NAME} configuration file (default: {' or '.join(DEFAULT_CONFIG_PATHS)})",
)
subparsers = parser.add_subparsers(title="commands")

parser_state_show_highstate = subparsers.add_parser(
    "highstate", help="renders the states for the specified minions"
)
parser_state_show_highstate.add_argument("minion_id", nargs="*")
parser_state_show_highstate.set_defaults(func=state.show_highstate)

parser_pillar_items = subparsers.add_parser(
    "pillars", help="renders pillar items for the specified minions"
)
parser_pillar_items.add_argument("minion_id", nargs="*")
parser_pillar_items.set_defaults(func=pillar.items)


args = parser.parse_args()
config = Config(args)
if "func" in args:
    args.func(config)
else:
    parser.print_usage()
