import difflib
import json
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, cast
from unittest.mock import patch

import click
import salt.output
import salt.runners.saltutil
import salt.utils.yaml

import slskit.commands
import slskit.lib.logging
import slskit.pillar
import slskit.state
import slskit.template
from slskit import PACKAGE_NAME, VERSION
from slskit.opts import DEFAULT_CONFIG_PATHS, DEFAULT_SNAPSHOT_PATH, Config
from slskit.types import MinionDict


@click.group()
@click.version_option(version=VERSION)
@click.option(
    "-c",
    "--config",
    "config_path",
    help=(
        f"path to {PACKAGE_NAME} configuration file "
        f"(default: {' or '.join(DEFAULT_CONFIG_PATHS)})"
    ),
)
@click.option(
    "-l",
    "--log-level",
    default="WARNING",
    type=click.Choice(slskit.lib.logging.LEVEL_CHOICES),
)
@click.pass_context
def cli(ctx, config_path, log_level):
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path

    log_level = getattr(logging, log_level)
    slskit.lib.logging.basic_config(level=log_level)


@cli.command(help="render highstate for specified minions")
@click.argument("minion_id", nargs=-1)
@click.pass_context
def highstate(ctx, minion_id):
    config = Config(minion_id=minion_id, **ctx.obj)
    minion_dict = slskit.state.show_highstate(config)
    _output(minion_dict, config)


@cli.command(help="render a given sls for specified minions")
@click.argument("sls")
@click.argument("minion_id", nargs=-1)
@click.pass_context
def sls(ctx, sls, minion_id):
    config = Config(minion_id=minion_id, **ctx.obj)
    minion_dict = slskit.state.show_sls(sls, config)
    _output(minion_dict, config)


@cli.command(help="render pillar items for specified minions")
@click.argument("minion_id", nargs=-1)
@click.pass_context
def pillars(ctx, minion_id):
    config = Config(minion_id=minion_id, **ctx.obj)
    minion_dict = slskit.pillar.items(config)
    _output(minion_dict, config)


@cli.command(help="render a file template for specified minions")
@click.argument("path")
@click.argument("minion_id", nargs=-1)
@click.option(
    "--renderer", default="jinja", help="renderer to be used (default: jinja)",
)
@click.option(
    "--context",
    default="{}",
    type=json.loads,
    help="JSON object containing extra variables to be passed into the renderer",
)
@click.pass_context
def template(ctx, path, minion_id, renderer, context):
    config = Config(minion_id=minion_id, **ctx.obj)
    minion_dict = slskit.template.render(config, path, renderer, context)
    _output(minion_dict, config)


@cli.command(help="invoke saltutil.sync_all runner")
@click.pass_context
def refresh(ctx):
    config = Config(**ctx.obj)
    with patch("salt.runners.fileserver.__opts__", config.opts, create=True):
        salt.runners.fileserver.update()
    with patch("salt.runners.saltutil.__opts__", config.opts, create=True):
        salt.runners.saltutil.sync_all()


@cli.group()
@click.option(
    "-p",
    "--path",
    "snapshot_path",
    default=DEFAULT_SNAPSHOT_PATH,
    type=Path,
    help=f"path to snapshot file (default: {DEFAULT_SNAPSHOT_PATH})",
)
@click.pass_context
def snapshot(ctx, snapshot_path):
    ctx.obj["snapshot_path"] = snapshot_path


@snapshot.command(help="create highstate snapshot")
@click.pass_context
def create(ctx):
    config = Config(**ctx.obj)

    dump = _dump_highstate(config)
    if not dump:
        sys.exit("Failed to render snapshot")

    config.snapshot_path.write_text(dump)
    print(f"Snapshot saved as `{config.snapshot_path}`")


@snapshot.command(help="check highstate snapshot")
@click.pass_context
def check(ctx):
    config = Config(**ctx.obj)

    if not config.snapshot_path.exists():
        sys.exit(f"Snapshot file `{config.snapshot_path}` not found")
    snapshot = config.snapshot_path.read_text()

    dump = _dump_highstate(config)
    if not dump:
        sys.exit("Failed to render snapshot")

    if snapshot != dump:
        _display_diff(snapshot, dump)
        sys.exit(
            "There are some changes not present in the snapshot. "
            "Run `slskit snapshot create` to update the snapshot."
        )


def _output(minion_dict: MinionDict, config: Config) -> None:
    salt.output.display_output(minion_dict.output, opts=config.opts)
    if not minion_dict.all_valid:
        sys.exit(1)


def _dump_highstate(config: Config) -> Optional[str]:
    minion_dict = slskit.state.show_highstate(config)
    if not minion_dict.all_valid:
        return None

    dump = salt.utils.yaml.safe_dump(minion_dict.output, default_flow_style=False)
    return cast(str, dump)


def _display_diff(a: str, b: str) -> None:
    diff = difflib.unified_diff(
        a.splitlines(keepends=True), b.splitlines(keepends=True)
    )
    sys.stdout.writelines(diff)


cli()
