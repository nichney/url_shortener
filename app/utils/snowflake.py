from snowflake import SnowflakeGenerator

from app.utils.id_from_pod_name import get_node_id_from_pod_name


_generator = SnowflakeGenerator(get_node_id_from_pod_name())


def new_id() -> int:
    """
    Возвращает уникальный Snowflake ID.
    Использует глобальный экземпляр генератора для сохранения состояния последовательности.
    """
    try:
        return next(_generator)
    except StopIteration:
        raise RuntimeError("Snowflake ID generation limit reached for this millisecond")