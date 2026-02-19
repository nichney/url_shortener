import os
from contextlib import contextmanager


@contextmanager
def in_environment(pod_id=123, base_url="https://example.com", shards="default:postgresql://user:pass@localhost/db", redis="default:redis://localhost:6379"):
    env_variables = ["POD_NAME", "BASE_URL", "DB_SHARDS", "REDIS_SHARDS"]
   
    original_values = {
        name: value 
        for name, value in 
        zip(env_variables,  map(os.environ.get, env_variables))
        }

    os.environ["POD_NAME"] = "web-app-" + f"{pod_id}"
    os.environ["BASE_URL"] = base_url
    os.environ["DB_SHARDS"] = shards
    os.environ["REDIS_SHARDS"] = redis
    try:
        yield
    finally:
        for name in env_variables:
            if original_values[name]:
                os.environ[name] = original_values[name]
