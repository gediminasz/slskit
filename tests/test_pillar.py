from unittest.mock import Mock

import pytest

import salinity.pillar


@pytest.fixture
def args():
    return Mock(pillar_root="tests/project/pillar", pillar_top="top.sls")


def test_pillar_top(args):
    assert salinity.pillar.top(args) == {
        "*": {
            "minion_id": "GRAIN id",
            "grain_via_dict_access": "GRAIN id",
            "module": True,
        }
    }
