import salt.output
import salt.pillar

from .opts import Config
from .types import AnyDict, MinionDict, Result


def items(config: Config) -> MinionDict:
    return MinionDict(
        {
            minion_id: compile_pillar(
                opts=config.opts,
                grains=config.grains_for(minion_id),
                minion_id=minion_id,
            )
            for minion_id in config.minion_ids
        }
    )


def compile_pillar(opts: AnyDict, grains: AnyDict, minion_id: str) -> Result:
    pillar = salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()
    return Result(valid="_errors" not in pillar, value=pillar)
