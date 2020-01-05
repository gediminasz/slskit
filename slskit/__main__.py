import logging  # isort:skip
import colorlog  # isort:skip

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
)
logging.basicConfig(level=logging.WARNING, handlers=(handler,))


from argparse import ArgumentParser

from . import PACKAGE_NAME, pillar, state, system
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

highstateparser = subparsers.add_parser(
    "highstate", help="renders the states for the specified minions"
)
highstateparser.add_argument("minion_id", nargs="*")
highstateparser.set_defaults(func=state.show_highstate)

pillars_parser = subparsers.add_parser(
    "pillars", help="renders pillar items for the specified minions"
)
pillars_parser.add_argument("minion_id", nargs="*")
pillars_parser.set_defaults(func=pillar.items)

refresh_parser = subparsers.add_parser("refresh", help="invoke Salt fileserver update")
refresh_parser.set_defaults(func=system.refresh)

args = parser.parse_args()
config = Config(args)
if "func" in args:
    args.func(config)
else:
    parser.print_usage()
