import os

"""
commentary: now generator reads POD_NAME itself
pod_name = os.getenv("POD_NAME") #used by snowflake generator
"""
BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL is not set!")