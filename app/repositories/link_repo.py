from app.database.sharding import DatabaseManager
from app.database.models import Links


class LinkRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager


    async def create_link(self, original_url: str, short_id: str) -> str:
        with self.db.get_session(short_id) as session:
            new_link = Links(id=short_id, url=original_url)
            session.add(new_link)

            # autocommit on block exit
            return new_link.id


    async def get_link(self, short_id: str):
        with self.db.get_session(short_id) as session:
            link = session.get(Links, short_id)
            if not link:
                return None
            return link