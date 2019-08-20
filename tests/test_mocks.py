from unittest.mock import MagicMock

import pytest

from salinity.mocks import MockDict, MockGrains, MockVault


@pytest.fixture
def salt():
    return MockDict(vault=MockVault())


def test_salt_vault_read_secret(salt):
    value = salt["vault"].read_secret("path/to/secret", "key")
    assert value == "SECRET path/to/secret key"


def test_salt_vault_read_secret_without_key(salt):
    value = salt["vault"].read_secret("path/to/secret")
    assert value == {
        "SECRET path/to/secret one": "one",
        "SECRET path/to/secret two": "two",
    }


def test_salt_cmd_run(salt):
    assert isinstance(salt["cmd.run"]("whoami"), MagicMock)


def test_grains_get():
    assert MockGrains()["id"] == "GRAIN id"
