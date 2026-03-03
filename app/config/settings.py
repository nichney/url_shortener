import os
from pathlib import Path


class ProjectSettings:

    def __init__(self):
        self.base_url = self.get_base_url()
        self.db_shards = self.get_db_shards()
        self.redis_shards = self.get_redis_shards()
        self.pod_name = self.get_pod_name()
        self.app_title = "Сократитель ссылок"
        self.frontend_directory, self.index_page = self.get_frontend_dir()


    def get_base_url(self) -> str:
        """
            BASE_URL=https://example.com/
        """
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("BASE_URL is not set!")
        return base_url


    def get_db_shards(self) -> str:
        """
            Пример: DB_SHARDS=db1:postgresql://user:pass@host1/db;db2:postgresql://user:pass@host2/db
        """
        shards_str = os.getenv("DB_SHARDS")
        if not shards_str:
            raise ValueError("DB_SHARDS is not set!")
        return shards_str


    def get_redis_shards(self) -> str:
        """
            Формат: shardName:master_url|slave1_url,slave2_url;shardName2:...
            Пример: SHARD1:redis://m1:6379|redis://s1:6379;SHARD2:redis://m2:6379
        """
        cache_shards = os.getenv("REDIS_SHARDS")
        if not cache_shards:
            raise ValueError("REDIS_SHARDS is not set!")
        return cache_shards


    def get_pod_name(self) -> str:
        pod_name = os.getenv("POD_NAME")
        if not pod_name:
            raise ValueError("POD_NAME is not set!")
        return pod_name


    def get_frontend_dir(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        FRONTEND_DIR = BASE_DIR / "frontend"
        return (str(FRONTEND_DIR), str(FRONTEND_DIR / "index.html"))


_settings = None

def get_settings() -> ProjectSettings:
    global _settings
    if not _settings:
        _settings = ProjectSettings()
    return _settings