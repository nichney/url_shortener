import hashlib
import os

from app.config.settings import pod_name


def get_node_id_from_pod_name() -> int:
    hash_bytes = hashlib.sha256(pod_name.encode()).digest()
    hash_int = int.from_bytes(hash_bytes[:2], byteorder='big')
    return hash_int % 1024