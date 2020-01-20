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
    highstate = state.show_highstate(config)
    snapshot = {minion_id: result.value for minion_id, result in highstate.items()}
    dump = salt.utils.yaml.safe_dump(snapshot, default_flow_style=False)
    config.snapshot_path.write_text(dump)


def check_snapshot(config: Config):
    print("check_snapshot")


def _display_output(output: dict, config: Config):
    salt.output.display_output(output, out="yaml", opts=config.opts)
