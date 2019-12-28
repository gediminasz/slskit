import os

import yaml

import salt.config

DEFAULT_CONFIG_PATHS = ("salinity.yaml", "salinity.yml")


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
        }
    )

    config = load_settings(args.config)
    opts.update(config["salt"])

    return opts


def build_grains(args, minion_id):
    grains = {"id": minion_id}
    return grains


def load_settings(path):
    if path is not None:
        return load_yaml(path)

    for path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(path):
            return load_yaml(path)


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)
