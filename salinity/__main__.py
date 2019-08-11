from argparse import ArgumentParser

from salinity.utils import pretty_print
import salinity.pillar


def command(callable):
    return lambda args: pretty_print(callable(args))


parser = ArgumentParser(prog="salinity", description="Salinity - Salt testing toolkit.")
subparsers = parser.add_subparsers(title="command")

parser_pillar_top = subparsers.add_parser(
    "pillar.top", help="renders the pillar top file"
)
parser_pillar_top.set_defaults(func=command(salinity.pillar.top))

parser_pillar_items = subparsers.add_parser(
    "pillar.items", help="renders pillar items for the specified minions"
)
parser_pillar_items.add_argument("minion_id", nargs="+")
parser_pillar_items.set_defaults(func=command(salinity.pillar.items))

args = parser.parse_args()
args.func(args)
