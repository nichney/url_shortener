import os
from contextlib import contextmanager
from typing import Generator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.utils.hash_ring import HashRing
from app.database import models


class DatabaseManager:

    def __init__(self):
        """Пример: DB_SHARDS=db1:postgresql://user:pass@host1/db;db2:postgresql://user:pass@host2/db
        """
        shards_str = os.getenv("DB_SHARDS", "default:postgresql://user:pass@localhost/db")
        db_configs = {}
        for item in shards_str.split(';'):
            if ":" in item:
                name, url = item.split(":", 1)
                db_configs[name] = url

        self.hash_ring = HashRing(list(db_configs.keys()))
        self.engines = {name: create_async_engine(config) for name, config in db_configs.items()}
        self.session_factories = {}
        for name in self.engines:
            self.session_factories[name] = async_sessionmaker(
                bind=self.engines[name],
                class_=AsyncSession,
                autocommit=False,
                autoflush=False
            )


    def create_all_tables(self):
        for name, engine in self.engines.items():
            SQLModel.metadata.create_all(bind=engine)


    def _get_node_name(self, shard_key: str) -> str:
        return self.hash_ring.get_node(shard_key)


    @contextmanager
    def get_session(self, shard_key: str) -> Generator[Session, None, None]:
        """
        Контекстный менеджер для получения сессии нужного шарда.
        Гарантирует commit при успехе и rollback при ошибке.
        
        Использование:
        with db_manager.get_session("user_123") as session:
            user = session.get(User, "user_123")
            session.add(new_link)
        """
        node_name = self._get_node_name(shard_key)
        session_factory = self.session_factories[node_name]
        session = session_factory()
        
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_manager_instance: DatabaseManager | None = None

def get_db_manager() -> DatabaseManager:
    global db_manager_instance
    if db_manager_instance is None:
        db_manager_instance = DatabaseManager()
    return db_manager_instance