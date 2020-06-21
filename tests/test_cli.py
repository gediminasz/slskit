import subprocess


def execute(command):
    return subprocess.run(command.split(), capture_output=True).stdout.decode()


def test_template(snapshot):
    snapshot.assert_match(
        execute(
            "poetry run slskit template tests/project/salt/template/child.txt tester"
        ),
        "template.snap",
    )
