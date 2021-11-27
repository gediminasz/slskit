import subprocess

import pytest
import salt.version

SALT_VERSION = salt.version.__version_info__[0]


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
def test_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, check=True, capture_output=True)

    snapshot.assert_match(process.stdout.decode(), "stdout.snap")

    if SALT_VERSION == 3001:
        snapshot.assert_match(process.stderr.decode(), "stderr.3001.snap")
    else:
        snapshot.assert_match(process.stderr.decode(), "stderr.snap")
