import pickle
from typing import cast

from redis.asyncio import Redis

from ..constants import LOCATIONS_KEY_PREFIX, LOCATIONS_VERSIONS_KEY
from ..types import LocationRecord


async def get_locations(redis: Redis) -> list[LocationRecord]:
    versions = await redis.hgetall(LOCATIONS_VERSIONS_KEY)
    results: list[LocationRecord] = []
    ids = [key.decode() for key in versions.keys()]
    ids_chunked = [ids[i : i + 100] for i in range(0, len(ids), 100)]

    for ids_chunk in ids_chunked:
        keys = [f"{LOCATIONS_KEY_PREFIX}{obj_id}" for obj_id in ids_chunk]
        values = await redis.mget(keys)
        for value in values:
            if value:
                obj = cast(LocationRecord, pickle.loads(value))
                results.append(obj)

    return results
