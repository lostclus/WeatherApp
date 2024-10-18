import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from weatherapp_query.settings import settings
from weatherapp_query.storage.clickhouse import get_clickhouse_client


@pytest.fixture(autouse=True)
def app():
    from weatherapp_query.api import app

    return app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/query/api/v1",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def clickhouse_client():
    tables = ["weather"]
    work_db = settings.clickhouse_database
    test_db = f"test_{work_db}"

    async with get_clickhouse_client() as client:
        table_defs = []
        for table in tables:
            table_def = await client.fetchval(f"SHOW CREATE TABLE {table}")
            table_def = table_def.replace(
                f"CREATE TABLE {work_db}.", f"CREATE TABLE {test_db}."
            )
            table_defs.append(table_def)
        await client.execute(f"DROP DATABASE IF EXISTS {test_db}")
        await client.execute(f"CREATE DATABASE {test_db}")

    try:
        settings.clickhouse_database = test_db
        async with get_clickhouse_client(database=test_db) as test_client:
            for table_def in table_defs:
                await test_client.execute(table_def)

            yield test_client
    finally:
        settings.clickhouse_database = work_db
        async with get_clickhouse_client() as client:
            await client.execute(f"DROP DATABASE IF EXISTS {test_db}")
