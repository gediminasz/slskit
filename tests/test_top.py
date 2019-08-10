import pytest

from salinity.top import Top


def test_wildcard():
    top = Top({"*": {"foo": "bar"}})

    assert top.for_minion("stuart") == {"foo": "bar"}
