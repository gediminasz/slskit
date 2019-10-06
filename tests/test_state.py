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


def test_state_top(args):
    assert salinity.state.top(args) == {
        "*": {
            "hello": {"cmd.run": [{"name": 'echo "Hello, I\'m PILLAR.name!"'}]},
            "system_timezone": {"timezone.system": [{"name": "UTC"}]},
        },
        "roles:via_pillar": {
            "role_via_pillar": {"cmd.run": [{"name": 'echo "This is applied via pillar"'}]}
        }
    }


def test_state_top_given_clashing_name(args):
    args.state_root = "tests/project/salt_clashing"

    assert salinity.state.top(args) == {
        "*": {"clashing_name": {"test.bar": [{"name": "bar"}]}}
    }


def test_state_show(args):
    args.minion_id = ("stuart",)
    assert salinity.state.show(args) == {
        "stuart": {
            "hello": {"cmd.run": [{"name": 'echo "Hello, I\'m Stuart!"'}]},
            "system_timezone": {"timezone.system": [{"name": "UTC"}]},
        }
    }
