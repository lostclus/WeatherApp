from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from ..storage.clickhouse import ClickHouseClient, get_clickhouse_client


async def _get_clickhouse_client() -> AsyncIterator[ClickHouseClient]:
    async with get_clickhouse_client() as client:
        yield client


ClickHouseDep = Annotated[ClickHouseClient, Depends(_get_clickhouse_client)]
