from app.repositories.link_repo import LinkRepository
from app.database.sharding import get_db_manager


async def get_link_repo() -> LinkRepository:
    db_manager = get_db_manager()
    return LinkRepository(db_manager)