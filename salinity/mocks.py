from collections import defaultdict
from typing import Union
from unittest.mock import MagicMock


class PrettyMock(MagicMock):
    def __repr__(self):
        return (
            f"{self._mock_parent}.{self._mock_name}"
            if self._mock_parent
            else self._mock_name
        )


class MockDict(defaultdict):
    def __missing__(self, key):
        return MagicMock(name=key)


class MockVault:
    def read_secret(self, path: str, key: str = None) -> Union[str, dict]:
        if not key:
            return {f"SECRET {path} one": "one", f"SECRET {path} two": "two"}
        return f"SECRET {path} {key}"


class MockGrains:
    def __getitem__(self, key):
        return f"GRAIN {key}"
