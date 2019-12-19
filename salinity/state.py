import salt.config
import salt.state
import salt.output

import salinity.pillar
from salinity.renderer import Renderer
from salinity.top import Minion, Top


def show_highstate(args):
    opts = build_opts(args)

    result = {
        minion_id: compile_highstate({**opts, "id": minion_id})
        for minion_id in args.minion_id
    }

    salt.output.display_output(result, out="yaml", opts=opts)


def build_opts(args):
    opts = salt.config.apply_minion_config()
    opts.update(
        {
            "root_dir": ".salinity",
            "cachedir": ".salinity/cachedir",
            "pki_dir": ".salinity/pki_dir",
            "sock_dir": ".salinity/sock_dir",
            "log_file": ".salinity/log_file",
            "conf_file": ".salinity/conf_file",
            "state_events": False,
            "file_client": "local",
            "file_roots": {"base": [args.state_root]},
            "pillar_roots": {"base": [args.pillar_root]},
        }
    )
    return opts


def compile_highstate(opts):
    return salt.state.HighState(opts).compile_highstate()


def show(args):
    pillars = salinity.pillar.items(args)
    return {
        minion_id: _state_for_minion(args, minion_id, pillars[minion_id])
        for minion_id in args.minion_id
    }


def _state_for_minion(args, minion_id, pillar):
    context = {"pillar": pillar}
    renderer = Renderer(args.state_root, context)
    top = Top.load(args.state_root, args.state_top, renderer)
    return top.for_minion(Minion(minion_id, pillar))
