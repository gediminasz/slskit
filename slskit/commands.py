import salt.output

from . import pillar, state
from .opts import Config


def highstate(config: Config):
    result = state.show_highstate(config)
    display_output(result, config)


def pillars(config: Config):
    result = pillar.items(config)
    display_output(result, config)


def display_output(output: dict, config: Config):
    salt.output.display_output(output, out="yaml", opts=config.opts)
