import logging

import click

log = logging.getLogger("slskit")


def minion_id_argument():
    def callback(ctx, param, value):
        value = value or ctx.obj["config"].roster.keys()
        unknown_ids = set(value) - set(ctx.obj["config"].roster.keys())
        if unknown_ids:
            log.warning(f"Minion ids not found in roster: {', '.join(unknown_ids)}")
        return value

    return click.argument("minion_id", nargs=-1, callback=callback)
