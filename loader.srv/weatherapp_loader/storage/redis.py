import threading
from typing import cast

from redis.asyncio import ConnectionPool, Redis

from .. import settings

_local = threading.local()


def create_redis_pool() -> ConnectionPool:
    pool: ConnectionPool = ConnectionPool.from_url(
        settings.REDIS_STORAGE_URL, socket_keepalive=True
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


def get_redis(pool: ConnectionPool | None = None) -> Redis:
    if pool is None:
        pool = get_redis_pool()
    return Redis(connection_pool=pool)
