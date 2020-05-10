import logging  # isort:skip
import colorlog  # isort:skip

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
)
logging.basicConfig(level=logging.WARNING, handlers=(handler,))

from argparse import ArgumentParser
from pathlib import Path

from . import PACKAGE_NAME, commands
from .opts import DEFAULT_CONFIG_PATHS, DEFAULT_SNAPSHOT_PATH, Config

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
    "highstate", help="render highstate for specified minions"
)
highstate_parser.add_argument("minion_id", nargs="*")
highstate_parser.set_defaults(func=commands.highstate)

sls_parser = subparsers.add_parser(
    "sls", help="render a given sls for specified minions"
)
sls_parser.add_argument("sls")
sls_parser.add_argument("minion_id", nargs="*")
sls_parser.set_defaults(func=commands.sls)

pillars_parser = subparsers.add_parser(
    "pillars", help="render pillar items for specified minions"
)
pillars_parser.add_argument("minion_id", nargs="*")
pillars_parser.set_defaults(func=commands.pillars)

refresh_parser = subparsers.add_parser(
    "refresh", help="invoke saltutil.sync_all runner"
)
refresh_parser.set_defaults(func=commands.refresh)

snapshot_parser = subparsers.add_parser(
    "snapshot", help="create and check highstate snapshots"
)
snapshot_parser.add_argument(
    "-p",
    "--path",
    default=DEFAULT_SNAPSHOT_PATH,
    type=Path,
    help=f"path to snapshot file (default: {DEFAULT_SNAPSHOT_PATH})",
    dest="snapshot_path",
)
snapshot_subparsers = snapshot_parser.add_subparsers(title="subcommands")
snapshot_create_parser = snapshot_subparsers.add_parser(
    "create", help="create highstate snapshot"
)
snapshot_create_parser.set_defaults(func=commands.create_snapshot, minion_id=None)
snapshot_check_parser = snapshot_subparsers.add_parser(
    "check", help="check highstate snapshot"
)
snapshot_check_parser.set_defaults(func=commands.check_snapshot, minion_id=None)

args = parser.parse_args()
config = Config(args)
args.func(config)
