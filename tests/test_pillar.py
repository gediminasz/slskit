from unittest.mock import Mock

import pytest

import salinity.pillar


@pytest.fixture
def args():
    return Mock(pillar_root="tests/project/pillar", pillar_top="top.sls")


def test_pillar_top(args):
    assert salinity.pillar.top(args) == {
        "*": {
            "minion_id": "GRAIN.id",
            "grain_via_dict_access": "GRAIN.id",
            "module": True,
            "secret": "SECRET foo/bar/baz qux",
            "prefixed_value": "prefix + GRAIN.host",
            "suffixed_value": "GRAIN.host + suffix",
        },
        "stuart": {"name": "Stuart"},
        "kevin": {"name": "Kevin"},
        "bob": {"name": "Bob"},
    }


def test_pillar_items(args):
    args.minion_id = ("stuart",)
    assert salinity.pillar.items(args) == {
        "stuart": {
            "minion_id": "GRAIN.id",
            "grain_via_dict_access": "GRAIN.id",
            "module": True,
            "secret": "SECRET foo/bar/baz qux",
            "name": "Stuart",
        }
    }
