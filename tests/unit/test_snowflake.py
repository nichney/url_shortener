import pytest
from tests.confest import in_pod


def test_new_id_returns_int():
    with in_pod():
        from app.utils.snowflake import new_id
        uid = new_id()
        assert isinstance(uid, int)
        assert uid > 0


def test_new_id_sequential_uniqueness():
    with in_pod():
        from app.utils.snowflake import new_id
        id1 = new_id()
        id2 = new_id()
        assert id1 != id2