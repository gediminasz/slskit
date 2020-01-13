import logging  # isort:skip
import colorlog  # isort:skip

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
)
logging.basicConfig(level=logging.WARNING, handlers=(handler,))

from argparse import ArgumentParser

from . import PACKAGE_NAME, commands
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
parser.set_defaults(func=lambda _: parser.print_usage())
subparsers = parser.add_subparsers(title="commands")

highstate_parser = subparsers.add_parser(
    "highstate", help="renders the states for the specified minions"
)
highstate_parser.add_argument("minion_id", nargs="*")
highstate_parser.set_defaults(func=commands.highstate)

pillars_parser = subparsers.add_parser(
    "pillars", help="renders pillar items for the specified minions"
)
pillars_parser.add_argument("minion_id", nargs="*")
pillars_parser.set_defaults(func=commands.pillars)

refresh_parser = subparsers.add_parser(
    "refresh", help="invoke saltutil.sync_all runner"
)
refresh_parser.set_defaults(func=commands.refresh)

args = parser.parse_args()
config = Config(args)
args.func(config)
