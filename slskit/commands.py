import difflib
import sys
from typing import Optional, cast
from unittest.mock import patch

import salt.output
import salt.runners.saltutil
import salt.utils.yaml

import slskit.pillar
import slskit.state
import slskit.template

from .opts import Config
from .types import MinionDict


def highstate(config: Config) -> None:
    minion_dict = slskit.state.show_highstate(config)
    _output(minion_dict, config)


def sls(config: Config) -> None:
    minion_dict = slskit.state.show_sls(config)
    _output(minion_dict, config)


def pillars(config: Config) -> None:
    minion_dict = slskit.pillar.items(config)
    _output(minion_dict, config)


def template(config: Config) -> None:
    minion_dict = slskit.template.render(config)
    _output(minion_dict, config)


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
