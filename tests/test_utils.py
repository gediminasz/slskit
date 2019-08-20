from salinity.utils import merge


def test_merge():
    assert merge({"a": 1}, {"a": 2}) == {"a": 2}


def test_merge_with_none():
    assert merge({"a": 1}, None) == {"a": 1}
