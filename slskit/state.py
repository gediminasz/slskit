from typing import List

import salt.output
import salt.state
import salt.utils

from slskit.lib.logging import log_errors

from .opts import Config
from .types import AnyDict, MinionDict, Result


def show_highstate(minion_ids: List[str], config: Config) -> MinionDict:
    return MinionDict(
        {
            minion_id: compile_highstate(
                {**config.opts, "id": minion_id, "grains": config.grains_for(minion_id)}
            )
            for minion_id in minion_ids
        }
    )


def compile_highstate(opts: AnyDict) -> Result:
    highstate = salt.state.HighState(opts)

    top = highstate.get_top()
    top_errors = highstate.verify_tops(top)

    matches = highstate.top_matches(top)
    if not highstate._check_pillar():
        log_errors(
            f"Failed to render pillar for {opts['id']}:",
            highstate.opts["pillar"]["_errors"],
        )
        return Result(False, highstate.opts["pillar"]["_errors"])

    result, render_errors = highstate.render_highstate(matches)

    errors = top_errors + render_errors
    if errors:
        log_errors(f"Failed to render highstate for {opts['id']}:", errors)

    return Result(False, errors) if errors else Result(True, result)


def show_sls(minion_ids: List[str], sls: str, config: Config) -> MinionDict:
    names = salt.utils.args.split_input(sls)
    return MinionDict(
        {
            minion_id: compile_sls(
                names,
                opts={
                    **config.opts,
                    "id": minion_id,
                    "grains": config.grains_for(minion_id),
                },
            )
            for minion_id in minion_ids
        }
    )


def compile_sls(names: List[str], opts: AnyDict) -> Result:
    highstate = salt.state.HighState(opts)
    result, errors = highstate.render_highstate({"base": names})
    return Result(False, errors) if errors else Result(True, result)
