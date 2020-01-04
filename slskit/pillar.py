import salt.output
import salt.pillar

from .opts import Config


def items(config: Config):
    result = {
        minion_id: compile_pillar(
            opts=config.opts, grains=config.grains_for(minion_id), minion_id=minion_id
        )
        for minion_id in config.minion_ids
    }

    salt.output.display_output(result, out="yaml", opts=config.opts)


def compile_pillar(opts, grains, minion_id):
    return salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()
