import os
import redis
from typing import Optional
from app.utils.hash_ring import HashRing


class RedisShard:

    def __init__(self, master_url: str, slave_urls: list[str] = None):
        self.master = redis.from_url(master_url, decode_responses=True)
        self.slaves = [
            redis.from_url(url, decode_responses=True) 
            for url in (slave_urls or [master_url])
        ]
        self._slave_idx = 0


    def get_read_node(self):
        node = self.slaves[self._slave_idx]
        self._slave_idx = (self._slave_idx + 1) % len(self.slaves)
        return node


class RedisManager:

    def __init__(self):
        """
        Формат: shardName:master_url|slave1_url,slave2_url;shardName2:...
        Пример: SHARD1:redis://m1:6379|redis://s1:6379;SHARD2:redis://m2:6379
        """
        raw_config = os.getenv("REDIS_SHARDS", "default:redis://localhost:6379")
        self.shards = {}
        
        for item in raw_config.split(';'):
            if ":" in item:
                shard_name, nodes = item.split(":", 1)
                parts = nodes.split("|")
                master_url = parts[0]
                slave_urls = parts[1].split(",") if len(parts) > 1 else [master_url]
                
                self.shards[shard_name] = RedisShard(master_url, slave_urls)

        self.hash_ring = HashRing(list(self.shards.keys()))


    def _get_shard(self, key: str) -> RedisShard:
        shard_name = self.hash_ring.get_node(key)
        return self.shards[shard_name]


    def set_value(self, key: str, value: str, ex: int = None):
        shard = self._get_shard(key)
        return shard.master.set(key, value, ex=ex)


    def get_value(self, key: str) -> Optional[str]:
        shard = self._get_shard(key)
        return shard.get_read_node().get(key)


redis_manager_instance: RedisManager | None = None

def get_redis_manager() -> RedisManager:
    global redis_manager_instance
    if redis_manager_instance is None:
        redis_manager_instance = RedisManager()
    return redis_manager_instance