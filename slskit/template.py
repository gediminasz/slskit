from typing import List

import salt.loader
import salt.template

import slskit.pillar
from slskit.opts import Config
from slskit.types import AnyDict, MinionDict, Result


def render(
    minion_ids: List[str], config: Config, path: str, renderer: str, context: AnyDict
) -> MinionDict:
    return MinionDict(
        {
            minion_id: render_template(config, minion_id, path, renderer, context)
            for minion_id in minion_ids
        }
    )


def render_template(
    config: Config, minion_id: str, path: str, renderer: str, context: AnyDict
) -> Result:
    grains = config.grains_for(minion_id)
    pillar = slskit.pillar.compile_pillar(config.opts, grains, minion_id).value
    opts = {**config.opts, "grains": grains, "pillar": pillar}

    functions = salt.loader.minion_mods(config.opts)
    renderers = salt.loader.render(opts, functions)

    output = salt.template.compile_template(
        template=path,
        renderers=renderers,
        default=renderer,
        blacklist=config.opts["renderer_blacklist"],
        whitelist=config.opts["renderer_whitelist"],
        **context
    )

    valid = output != {}
    value = output.read() if hasattr(output, "read") else output
    return Result(valid=valid, value=value)
