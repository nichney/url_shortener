import os
from contextlib import contextmanager

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