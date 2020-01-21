import difflib
import sys
from pathlib import Path
from unittest.mock import patch

import salt.output
import salt.runners.saltutil
import salt.utils.yaml
from salt.fileserver import Fileserver

from . import pillar, state
from .opts import Config


def highstate(config: Config):
    highstate = state.show_highstate(config)

    output = {minion_id: result.value for minion_id, result in highstate.items()}
    _display_output(output, config)

    if not all(r.valid for r in highstate.values()):
        sys.exit(1)


def pillars(config: Config):
    result = pillar.items(config)
    _display_output(result, config)

    if any("_errors" in pillar for pillar in result.values()):
        sys.exit(1)


def refresh(config: Config):
    with patch("salt.runners.saltutil.__opts__", config.opts, create=True):
        salt.runners.saltutil.sync_all()


def create_snapshot(config: Config):
    dump = _dump_highstate(config)
    config.snapshot_path.write_text(dump)


def check_snapshot(config: Config):
    if not config.snapshot_path.exists():
        sys.exit(f"Snapshot file {config.snapshot_path} not found")

    snapshot = config.snapshot_path.read_text()
    current = _dump_highstate(config)

    if snapshot != current:
        _display_diff(snapshot, current)
        sys.exit(1)


def _dump_highstate(config: Config) -> str:
    highstate = state.show_highstate(config)
    snapshot = {minion_id: result.value for minion_id, result in highstate.items()}
    return salt.utils.yaml.safe_dump(snapshot, default_flow_style=False)


def _display_diff(a: str, b: str):
    diff = difflib.unified_diff(
        a.splitlines(keepends=True), b.splitlines(keepends=True)
    )
    sys.stdout.writelines(diff)


def _display_output(output: dict, config: Config):
    salt.output.display_output(output, out="yaml", opts=config.opts)
