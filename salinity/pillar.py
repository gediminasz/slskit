import salt.output
import salt.pillar

from salinity.opts import build_opts


def items(args):
    opts = build_opts(args)

    result = {
        minion_id: compile_pillar(opts, {}, minion_id) for minion_id in args.minion_id
    }

    salt.output.display_output(result, out="yaml", opts=opts)


def compile_pillar(opts, grains, minion_id):
    return salt.pillar.get_pillar(opts, grains, minion_id).compile_pillar()
