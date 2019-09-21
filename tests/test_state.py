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


def test_state_top_given_clashing_name(args):
    args.state_root = "tests/project/salt_clashing"

    assert salinity.state.top(args) == {
        "*": {"clashing_name": {"test.bar": [{"name": "bar"}]}}
    }
