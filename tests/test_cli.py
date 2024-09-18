import os
import subprocess

import pytest
import salt.version

SALT_VERSION = salt.version.__saltstack_version__.major


@pytest.mark.parametrize(
    "command",
    (
        "poetry run slskit --version",
        "poetry run slskit highstate",
        "poetry run slskit sls detached",
        "poetry run slskit pillars",
        (
            "poetry run slskit --salt-output nested template tests/project/salt/template/child.txt "
            "tester --context '{\"foo\": 1234}'"
        ),
    ),
)
def test_successful_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, check=True, capture_output=True)
    assert process.returncode == 0
    snapshot.assert_match(process.stdout.decode(), f"stdout.{SALT_VERSION}.snap")


@pytest.mark.parametrize(
    "command",
    (
        "poetry run slskit sls errors.missing_colon tester",
        "poetry run slskit sls errors.undefined_variable tester",
    ),
)
def test_failed_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, check=False, capture_output=True)
    assert process.returncode == 1
    snapshot.assert_match(process.stdout.decode(), "stdout.snap")
