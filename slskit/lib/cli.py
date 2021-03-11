import logging
from typing import Any, Callable, Iterable, TypeVar

import click

log = logging.getLogger("slskit")

Function = TypeVar("Function", bound=Callable[..., Any])


def minion_id_argument() -> Callable[[Function], Function]:
    def callback(ctx: click.Context, _: Any, value: Iterable[str]) -> Iterable[str]:
        value = value or ctx.obj["config"].roster.keys()
        unknown_ids = set(value) - set(ctx.obj["config"].roster.keys())
        if unknown_ids:
            log.warning("Minion ids not found in roster: %s", ", ".join(unknown_ids))
        return value

    return click.argument("minion_id", nargs=-1, callback=callback)
