import hashlib
import os


def get_node_id_from_pod_name() -> int:
    pod_name = os.environ.get("POD_NAME", "")
    if not pod_name:
        raise RuntimeError("POD_NAME environment variable is not set")
    hash_bytes = hashlib.sha256(pod_name.encode()).digest()
    hash_int = int.from_bytes(hash_bytes[:2], byteorder='big')
    return hash_int % 1024