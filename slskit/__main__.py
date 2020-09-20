import difflib
import json
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
@click.option(
    "-c",
    "--config",
    help=(
        f"path to {PACKAGE_NAME} configuration file "
        f"(default: {' or '.join(DEFAULT_CONFIG_PATHS)})"
    ),
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


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


def _output(minion_dict: MinionDict, config: Config) -> None:
    salt.output.display_output(minion_dict.output, opts=config.opts)
    if not minion_dict.all_valid:
        sys.exit(1)


cli()
