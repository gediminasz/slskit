from typing import Any, Dict, cast

import salt.output
import salt.pillar

from .opts import Config
from .types import AnyDict


def items(config: Config) -> Dict[str, AnyDict]:
    return {
        minion_id: compile_pillar(
            opts=config.opts, grains=config.grains_for(minion_id), minion_id=minion_id
        )
        for minion_id in config.minion_ids
    }


def compile_pillar(opts: AnyDict, grains: AnyDict, minion_id: str) -> AnyDict:
    pillar = salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()
    return cast(AnyDict, pillar)
