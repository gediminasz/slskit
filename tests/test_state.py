from unittest.mock import Mock

import pytest

import salinity.state


@pytest.fixture
def args():
    return Mock(
        state_root="tests/project/salt",
        state_top="top.sls",
        pillar_root="tests/project/pillar",
        pillar_top="top.sls",
    )


def test_state_show(args):
    args.minion_id = ("stuart",)
    assert salinity.state.show(args) == {
        "stuart": {
            "hello": {"cmd.run": [{"name": 'echo "Hello, I\'m Stuart!"'}]},
            "system_timezone": {"timezone.system": [{"name": "UTC"}]},
        }
    }
