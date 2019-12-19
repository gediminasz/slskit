import salt.config


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
