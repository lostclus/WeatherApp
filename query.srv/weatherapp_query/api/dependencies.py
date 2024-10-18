from typing import TYPE_CHECKING, Annotated

if not TYPE_CHECKING:
    from aioch import Client
else:
    from weatherapp.stubs.clickhouse import Client


from fastapi import Depends

from ..settings import settings


def get_clickhouse() -> Client:
    client = Client(
        host=settings.clickhouse_host,
        database=settings.clickhouse_database,
        user=settings.clickhouse_user,
        password=settings.clickhouse_password,
    )
    return client


ClickHouseDep = Annotated[Client, Depends(get_clickhouse)]
