import pytest
import os
from contextlib import contextmanager

from app.utils.id_from_pod_name import get_node_id_from_pod_name


@contextmanager
def in_pod(pod_id=123):
    original_val = os.environ.get("POD_NAME")
    os.environ["POD_NAME"] = "web-app-" + f"{pod_id}"
    try:
        yield
    finally:
        if original_val is None:
            del os.environ["POD_NAME"]
        else:
            os.environ["POD_NAME"] = original_val


def test_node_id_is_consistent():
    with in_pod():
        id1 = get_node_id_from_pod_name()
        id2 = get_node_id_from_pod_name()
    
        assert id1 == id2
        assert 0 <= id1 < 1024


def test_node_id_different_for_different_pods():
    with in_pod(pod_id=123):
        id_alpha = get_node_id_from_pod_name()
    
    with in_pod(pod_id=124):
        id_beta = get_node_id_from_pod_name()
    
    assert id_alpha != id_beta