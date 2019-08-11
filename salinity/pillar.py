from salinity.top import Top


def top(args):
    return Top.load("pillar").body


def items(args):
    top = Top.load("pillar")
    return {minion_id: top.for_minion(minion_id) for minion_id in args.minion_id}
