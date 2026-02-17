import pytest
from tests.conftest import in_pod

from app.utils.id_from_pod_name import get_node_id_from_pod_name


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