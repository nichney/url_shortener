import hashlib
import os

from app.config.settings import get_settings


def get_node_id_from_pod_name() -> int:
    pod_name = get_settings().pod_name
    hash_bytes = hashlib.sha256(pod_name.encode()).digest()
    hash_int = int.from_bytes(hash_bytes[:2], byteorder='big')
    return hash_int % 1024