import logging
from unittest.mock import Mock

import pytest

from slskit.opts import Config


@pytest.mark.parametrize(
    "value,expected_output", (("warning", logging.WARNING), ("debug", logging.DEBUG)),
)
def test_config_log_level(value, expected_output):
    args = Mock(name="args", log_level=value)
    assert Config(args).log_level == expected_output
