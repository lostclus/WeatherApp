import pickle
from typing import cast

from redis.asyncio import Redis

from ..types import LocationRecord

_VERSIONS_KEY = "locations"
_KEY_PREFIX = "location:"


async def get_locations(redis: Redis) -> list[LocationRecord]:
    versions = await redis.hgetall(_VERSIONS_KEY)
    results: list[LocationRecord] = []
    ids = list(versions.keys())
    ids_chunked = [ids[i : i + 100] for i in range(0, len(ids), 100)]

    for ids_chunk in ids_chunked:
        keys = [f"{_KEY_PREFIX}{obj_id}" for obj_id in ids_chunk]
        values = await redis.mget(keys)
        for value in values:
            if value:
                obj = cast(LocationRecord, pickle.loads(value))
                results.append(obj)

    return results
