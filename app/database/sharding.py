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
        self.sessions = {}

    def get_session(self, shard_key: str):
        node = self.hash_ring.get_node(shard_key)
        if node not in self.sessions:
            Session = sessionmaker(bind=self.engines[node])
            self.sessions[node] = Session()
        return self.sessions[node]

    def execute_query(self, shard_key, query_func):
        """Пример использования: 
        result = db_manager.execute_query(
            shard_key='user_123',
            query_func=lambda session: session.query(User).filter_by(id=123).first()
        )
        """
        session = self.get_session(shard_key)
        try:
            result = query_func(session)
            session.commit()
            return result
        except:
            session.rollback()
            raise