import salt.output
import salt.state

from .opts import Config


def show_highstate(config: Config):
    result = {
        minion_id: compile_highstate(
            {**config.opts, "id": minion_id, "grains": config.grains_for(minion_id)}
        )
        for minion_id in config.minion_ids
    }

    salt.output.display_output(result, out="yaml", opts=config.opts)


def compile_highstate(opts):
    return salt.state.HighState(opts).compile_highstate()
