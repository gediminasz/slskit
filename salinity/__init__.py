import logging
import runpy

import colorlog


def run_module():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
    )
    logging.basicConfig(level=logging.WARNING, handlers=(handler,))

    runpy.run_module("salinity")
