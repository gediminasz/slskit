import argparse
import os
from dataclasses import dataclass

import jsonschema
import salt.config
import yaml
from funcy import cached_property, get_in, post_processing

from . import PACKAGE_NAME

DEFAULT_CONFIG_PATHS = (f"{PACKAGE_NAME}.yaml", f"{PACKAGE_NAME}.yml")

SCHEMA = {
    "type": "object",
    "properties": {
        "salt": {"type": "object"},
        PACKAGE_NAME: {
            "type": "object",
            "properties": {
                "roster": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {"grains": {"type": "object"}},
                    },
                }
            },
        },
    },
}


def validate(instance, schema=SCHEMA):
    jsonschema.validate(instance, schema)
    return instance


@dataclass
class Config:
    args: argparse.Namespace

    @cached_property
    def opts(self):
        opts = salt.config.apply_minion_config()
        root_dir = f".{PACKAGE_NAME}"
        opts.update(
            {
                "root_dir": root_dir,
                "cachedir": f"{root_dir}/cachedir",
                "pki_dir": f"{root_dir}/pki_dir",
                "sock_dir": f"{root_dir}/sock_dir",
                "log_file": f"{root_dir}/log_file",
                "conf_file": f"{root_dir}/conf_file",
                "state_events": False,
                "file_client": "local",
            }
        )
        opts.update(self.settings.get("salt", {}))
        return opts

    @cached_property
    def minion_ids(self):
        return self.args.minion_id or self.roster.keys()

    @cached_property
    def roster(self):
        return self._get_setting(f"{PACKAGE_NAME}.roster", {})

    @cached_property
    @post_processing(validate)
    def settings(self):
        if self.args.config is not None:
            return load_yaml(self.args.config)
        for path in DEFAULT_CONFIG_PATHS:
            if os.path.exists(path):
                return load_yaml(path)
        return {}

    def grains_for(self, minion_id):
        grains = self._get_setting(f"{PACKAGE_NAME}.roster.{minion_id}.grains", {})
        return {"id": minion_id, **grains}

    def _get_setting(self, path, default, separator="."):
        return get_in(self.settings, path.split(separator), default)


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)
