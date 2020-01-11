from dataclasses import dataclass
from typing import Dict

import salt.output
import salt.state

from .opts import Config


@dataclass(frozen=True)
class Highstate:
    valid: bool
    value: object


def show_highstate(config: Config) -> Dict[str, Highstate]:
    return {
        minion_id: compile_highstate(
            {**config.opts, "id": minion_id, "grains": config.grains_for(minion_id)}
        )
        for minion_id in config.minion_ids
    }


def compile_highstate(opts: dict) -> Highstate:
    highstate = salt.state.HighState(opts)

    top = highstate.get_top()
    top_errors = highstate.verify_tops(top)

    matches = highstate.top_matches(top)
    result, render_errors = highstate.render_highstate(matches)

    errors = top_errors + render_errors
    return Highstate(False, errors) if errors else Highstate(True, result)
