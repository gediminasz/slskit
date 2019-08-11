from salinity.top import Top


def top(args):
    return Top.load(args.pillar_root, args.pillar_top).body


def items(args):
    top = Top.load(args.pillar_root, args.pillar_top)
    return {minion_id: top.for_minion(minion_id) for minion_id in args.minion_id}
