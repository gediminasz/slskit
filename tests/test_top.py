import pytest

from salinity.top import Block, Minion


def test_wildcard_matching():
    block = Block("*", [], None)
    minion = Minion("stuart")
    assert block.matches(minion)
