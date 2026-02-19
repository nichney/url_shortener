from app.repositories.link_repo import LinkRepository
from app.database.cache import RedisManager
from app.database.sharding import get_db_manager
from app.database.cache import get_redis_manager


async def get_link_repo() -> LinkRepository:
    db_manager = get_db_manager()
    return LinkRepository(db_manager)


async def get_redis_repo() -> RedisManager:
    redis_manager = get_redis_manager()
    return redis_manager