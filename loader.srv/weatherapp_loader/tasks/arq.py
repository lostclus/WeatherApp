import threading
from typing import cast

from arq import ArqRedis
from redis.asyncio import ConnectionPool

from .. import settings

_local = threading.local()


def create_redis_pool() -> ConnectionPool:
    pool: ConnectionPool = ConnectionPool.from_url(
        settings.REDIS_QUEUE_URL, socket_keepalive=True
    )
    return pool


def get_redis_pool() -> ConnectionPool:
    pool = cast(ConnectionPool | None, getattr(_local, "pool", None))
    if pool is not None:
        return pool
    _local.pool = create_redis_pool()
    return _local.pool


async def close_redis_pool() -> None:
    if not hasattr(_local, "pool"):
        return
    await _local.pool.disconnect()
    del _local.pool


def get_arq_pool(
    arq_redis: ArqRedis | None = None,
    redis_pool: ConnectionPool | None = None,
) -> ArqRedis:
    if arq_redis is not None:
        return arq_redis

    if redis_pool is None:
        redis_pool = get_redis_pool()

    pool = ArqRedis(redis_pool)
    return pool
