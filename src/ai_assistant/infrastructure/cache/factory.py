"""Модуль с фабрикой Redis."""

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from ai_assistant.config import Config
from ai_assistant.infrastructure.cache import RedisMemoryRepository


def get_redis_connection_pool(config: Config) -> ConnectionPool:
    """Создает и возвращает ConnectionPool."""
    return ConnectionPool.from_url(url=config.redis_url)


def get_redis_client_with_connection_pool(pool: ConnectionPool) -> Redis:
    """Создает и возвращает Redis с ConnectionPool."""
    return Redis(connection_pool=pool)


def get_memory_repository(
    redis: Redis,
    history_limit: int,
) -> RedisMemoryRepository:
    """Создает и возвращает экземпляр IMemoryRepository."""
    return RedisMemoryRepository(redis_client=redis, history_limit=history_limit)
