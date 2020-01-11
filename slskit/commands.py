import salt.output

from . import state
from .opts import Config


def highstate(config: Config):
    result = state.show_highstate(config)
    display_output(result, config)


def display_output(output: dict, config: Config):
    salt.output.display_output(output, out="yaml", opts=config.opts)
