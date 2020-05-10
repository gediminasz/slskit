from dataclasses import dataclass
from typing import Any, Dict

import salt.output
import salt.state

from .opts import Config
from .types import AnyDict


@dataclass(frozen=True)
class Highstate:  # TODO GZL Result
    valid: bool
    value: Any


def show_highstate(config: Config) -> Dict[str, Highstate]:
    return {
        minion_id: compile_highstate(
            {**config.opts, "id": minion_id, "grains": config.grains_for(minion_id)}
        )
        for minion_id in config.minion_ids
    }


def compile_highstate(opts: AnyDict) -> Highstate:
    highstate = salt.state.HighState(opts)

    top = highstate.get_top()
    top_errors = highstate.verify_tops(top)

    matches = highstate.top_matches(top)
    result, render_errors = highstate.render_highstate(matches)

    errors = top_errors + render_errors
    return Highstate(False, errors) if errors else Highstate(True, result)


def show_sls(config: Config) -> AnyDict:
    return {
        minion_id: compile_sls(
            config.args.sls,
            {**config.opts, "id": minion_id, "grains": config.grains_for(minion_id)},
        )
        for minion_id in config.minion_ids
    }


# TODO GZL names
def compile_sls(name, opts: AnyDict) -> AnyDict:
    highstate = salt.state.HighState(opts)
    result, errors = highstate.render_highstate({"base": [name]})
    return Highstate(False, errors) if errors else Highstate(True, result)
