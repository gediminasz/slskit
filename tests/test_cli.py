import os
import subprocess

import pytest


@pytest.mark.parametrize(
    "command",
    (
        "poetry run slskit --version",
        "poetry run slskit highstate",
        "poetry run slskit --log-level INFO highstate",
        "poetry run slskit sls detached",
        "poetry run slskit pillars",
        (
            "poetry run slskit template tests/project/salt/template/child.txt "
            "tester --context '{\"foo\": 1234}'"
        ),
    ),
)
def test_successful_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, check=True, capture_output=True)
    assert process.returncode == 0
    snapshot.assert_match(process.stdout.decode(), "stdout.snap")


def test_stderr_output_snapshot(snapshot):
    process = subprocess.run(
        "poetry run slskit --log-level INFO highstate",
        shell=True,
        check=True,
        capture_output=True,
        env=dict(os.environ, PYTHONWARNINGS="ignore"),
    )
    assert process.returncode == 0
    snapshot.assert_match(process.stderr.decode(), "stderr.snap")


@pytest.mark.parametrize(
    "command",
    (
        "poetry run slskit sls errors.missing_colon tester",
        "poetry run slskit sls errors.undefined_variable tester",
    ),
)
def test_failed_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, capture_output=True)
    assert process.returncode == 1
    snapshot.assert_match(process.stdout.decode(), "stdout.snap")
