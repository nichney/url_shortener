import pytest

from app.utils.base62 import to_base62, from_base62


def test_inversiveness():
    test_numbers = [1, 61, 62, 100, 12345, 999999999]
    for num in test_numbers:
        encoded = to_base62(num)
        decoded = from_base62(encoded)
        assert decoded == num


def test_zero():
    assert to_base62(0) == '0'
    assert from_base62('0') == 0


def test_large_digits():
    large_num = 2**63 - 1 # largest 64 bit digit
    encoded = to_base62(large_num)
    assert from_base62(encoded) == large_num


def test_invalid_characters():
    with pytest.raises(KeyError):
        from_base62("@#")


def test_negative():
    with pytest.raises(ValueError):
        to_base62(-5)
