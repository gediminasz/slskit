import difflib
import sys
from pathlib import Path
from typing import Optional, cast
from unittest.mock import patch

import salt.output
import salt.runners.saltutil
import salt.utils.yaml
from salt.fileserver import Fileserver

from . import pillar, state
from .opts import Config
from .types import AnyDict


def highstate(config: Config) -> None:
    results = state.show_highstate(config)

    output = {minion_id: result.value for minion_id, result in results.items()}
    _display_output(output, config)

    if not all(r.valid for r in results.values()):
        sys.exit(1)


def sls(config: Config) -> None:
    results = state.show_sls(config)

    output = {minion_id: result.value for minion_id, result in results.items()}
    _display_output(output, config)

    if not all(r.valid for r in results.values()):
        sys.exit(1)


def pillars(config: Config) -> None:
    result = pillar.items(config)
    _display_output(result, config)

    if any("_errors" in pillar for pillar in result.values()):
        sys.exit(1)


def refresh(config: Config) -> None:
    with patch("salt.runners.saltutil.__opts__", config.opts, create=True):
        salt.runners.saltutil.sync_all()


def create_snapshot(config: Config) -> None:
    dump = _dump_highstate(config)
    if not dump:
        sys.exit("Failed to render snapshot")

    config.snapshot_path.write_text(dump)
    print(f"Snapshot saved as `{config.snapshot_path}`")


def check_snapshot(config: Config) -> None:
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


def _dump_highstate(config: Config) -> Optional[str]:
    highstate = state.show_highstate(config)
    if not all(r.valid for r in highstate.values()):
        return None

    snapshot = {minion_id: result.value for minion_id, result in highstate.items()}
    dump = salt.utils.yaml.safe_dump(snapshot, default_flow_style=False)
    return cast(str, dump)


def _display_diff(a: str, b: str) -> None:
    diff = difflib.unified_diff(
        a.splitlines(keepends=True), b.splitlines(keepends=True)
    )
    sys.stdout.writelines(diff)


def _display_output(output: AnyDict, config: Config) -> None:
    salt.output.display_output(output, out="yaml", opts=config.opts)
