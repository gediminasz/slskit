import salt.output
import salt.pillar

from .opts import Config


def items(config: Config) -> dict:
    return {
        minion_id: compile_pillar(
            opts=config.opts, grains=config.grains_for(minion_id), minion_id=minion_id
        )
        for minion_id in config.minion_ids
    }


def compile_pillar(opts: dict, grains: dict, minion_id: str) -> dict:
    return salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()
