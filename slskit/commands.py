import salt.output
from salt.fileserver import Fileserver

from . import pillar, state
from .opts import Config


def highstate(config: Config):
    result = state.show_highstate(config)
    _display_output(result, config)


def pillars(config: Config):
    result = pillar.items(config)
    _display_output(result, config)


def refresh(config: Config):
    Fileserver(config.opts).update()


def _display_output(output: dict, config: Config):
    salt.output.display_output(output, out="yaml", opts=config.opts)
