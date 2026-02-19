from fastapi.concurrency import run_in_threadpool

from app.repositories.link_repo import LinkRepository
from app.database.cache import RedisManager


async def get_link(repo: LinkRepository, redis_db: RedisManager, alias: str) -> str:
    cache_hit = await run_in_threadpool(redis_db.get_value, alias)
    if cache_hit:
        return cache_hit

    original_url = await run_in_threadpool(repo.get_link, alias)
    await run_in_threadpool(redis_db.set_value, alias, original_url, 3600)

    return original_url


