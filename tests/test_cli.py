import subprocess

import pytest


def execute(command):
    return


@pytest.mark.parametrize(
    "command",
    (
        "poetry run slskit highstate",
        "poetry run slskit sls detached",
        "poetry run slskit pillars",
        "poetry run slskit template tests/project/salt/template/child.txt tester",
    ),
)
def test_command_output_snapshot(command, snapshot):
    process = subprocess.run(command, shell=True, check=True, capture_output=True)
    output = process.stdout.decode()
    snapshot.assert_match(output, "output.snap")
