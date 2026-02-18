from app.repositories.link_repo import LinkRepository
from app.database.sharding import DatabaseManager


async def get_link_repo() -> LinkRepository:
    db_manager = DatabaseManager()
    return LinkRepository(db_manager)