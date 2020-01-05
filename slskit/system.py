from salt.fileserver import Fileserver

from .opts import Config


def refresh(config: Config):
    Fileserver(config.opts).update()
