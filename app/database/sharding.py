from contextlib import contextmanager
from typing import Generator
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

from app.utils.hash_ring import HashRing


class DatabaseManager:

    def __init__(self, db_configs: dict):
        """Пример db_configs: db_configs = {
            'db1': 'postgresql://user:pass@host1/dbname',
            'db2': 'postgresql://user:pass@host2/dbname', 
            'db3': 'postgresql://user:pass@host3/dbname'
            } 
        """
        self.hash_ring = HashRing(list(db_configs.keys()))
        self.engines = {name: create_engine(config) for name, config in db_configs.items()}
        self.session_factories = {}
        for name in self.engines:
            self.session_factories[name] = sessionmaker(
                bind=self.engines[name],
                class_=Session,
                autocommit=False,
                autoflush=False
            )


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
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()