from unittest.mock import Mock

import pytest

import salinity.state


@pytest.fixture
def args():
    return Mock(state_root="tests/project/salt", state_top="top.sls")


def test_state_top(args):
    assert salinity.state.top(args) == {
        "*": {
            "hello_world": {"cmd.run": [{"name": "echo Hello, world!"}]},
            "system_timezone": {"timezone.system": [{"name": "UTC"}]},
        }
    }
