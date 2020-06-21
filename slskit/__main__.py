import json
from argparse import ArgumentParser
from pathlib import Path

import slskit.commands
import slskit.lib.logging
from slskit import PACKAGE_NAME, VERSION
from slskit.opts import DEFAULT_CONFIG_PATHS, DEFAULT_SNAPSHOT_PATH, Config

parser = ArgumentParser(
    prog=PACKAGE_NAME,
    description=f"{PACKAGE_NAME} - tools for checking Salt state validity",
)
parser.add_argument("-V", "--version", action="version", version=VERSION)
parser.add_argument(
    "-c",
    "--config",
    help=(
        f"path to {PACKAGE_NAME} configuration file "
        f"(default: {' or '.join(DEFAULT_CONFIG_PATHS)})"
    ),
)
parser.add_argument(
    "-l", "--log-level", default="WARNING", choices=slskit.lib.logging.LEVEL_CHOICES
)
parser.set_defaults(func=lambda _: parser.print_usage())
subparsers = parser.add_subparsers(title="commands")

highstate_parser = subparsers.add_parser(
    "highstate", help="render highstate for specified minions"
)
highstate_parser.add_argument("minion_id", nargs="*")
highstate_parser.set_defaults(func=slskit.commands.highstate)

sls_parser = subparsers.add_parser(
    "sls", help="render a given sls for specified minions"
)
sls_parser.add_argument("sls")
sls_parser.add_argument("minion_id", nargs="*")
sls_parser.set_defaults(func=slskit.commands.sls)

pillars_parser = subparsers.add_parser(
    "pillars", help="render pillar items for specified minions"
)
pillars_parser.add_argument("minion_id", nargs="*")
pillars_parser.set_defaults(func=slskit.commands.pillars)

template_parser = subparsers.add_parser(
    "template", help="render a file template for specified minions"
)
template_parser.add_argument("path")
template_parser.add_argument("minion_id", nargs="*")
template_parser.add_argument(
    "--renderer", default="jinja", help="renderer to be used (default: jinja)",
)
template_parser.add_argument(
    "--context",
    default={},
    type=json.loads,
    help="JSON object containing extra variables to be passed into the renderer",
)
template_parser.set_defaults(func=slskit.commands.template)

refresh_parser = subparsers.add_parser(
    "refresh", help="invoke saltutil.sync_all runner"
)
refresh_parser.set_defaults(func=slskit.commands.refresh)

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
snapshot_create_parser.set_defaults(
    func=slskit.commands.create_snapshot, minion_id=None
)
snapshot_check_parser = snapshot_subparsers.add_parser(
    "check", help="check highstate snapshot"
)
snapshot_check_parser.set_defaults(func=slskit.commands.check_snapshot, minion_id=None)

args = parser.parse_args()
config = Config(args)

slskit.lib.logging.basic_config(level=config.log_level)

args.func(config)
