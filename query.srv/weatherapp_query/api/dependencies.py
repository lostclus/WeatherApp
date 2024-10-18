from typing import TYPE_CHECKING, Annotated, Any

if not TYPE_CHECKING:
    from aioch import Client
else:

    class Client:
        def __init__(**kwargs: Any):
            pass

        async def execute(
            self,
            sql: str,
            params: dict[str, Any] | None = None,
            settings: dict[str, Any] | None = None,
        ) -> Any:
            pass


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
