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
        "poetry run slskit sls errors.missing_colon tester",
    ),
)
def test_command_output_snapshot(command, snapshot):
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        env=dict(os.environ, PYTHONWARNINGS="ignore"),
    )
    snapshot.assert_match(process.stdout.decode(), "stdout.snap")
    snapshot.assert_match(process.stderr.decode(), "stderr.snap")
