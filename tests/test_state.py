from types import SimpleNamespace

import pytest
import salt.state

from slskit.opts import Config
from slskit.state import compile_highstate


@pytest.fixture
def args():
    return SimpleNamespace(config="slskit.yaml")


@pytest.fixture
def config(args):
    return Config(args)


def test_compile_highstate_is_equivalent_to_original_implementation(config):
    opts = {**config.opts, "id": "tester", "grains": config.grains_for("tester")}
    expected_value = salt.state.HighState(opts).compile_highstate()
    assert compile_highstate(opts).value == expected_value
