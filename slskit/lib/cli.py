import logging
from typing import Any, Iterable

import click

from slskit.types import Decorator

log = logging.getLogger("slskit")


def minion_id_argument() -> click.Argument:
    def callback(ctx: click.Context, _: Any, value: Iterable[str]) -> Decorator:
        print(ctx, _, value)
        value = value or ctx.obj["config"].roster.keys()
        unknown_ids = set(value) - set(ctx.obj["config"].roster.keys())
        if unknown_ids:
            log.warning("Minion ids not found in roster: %s", ", ".join(unknown_ids))
        return value

    return click.argument("minion_id", nargs=-1, callback=callback)
