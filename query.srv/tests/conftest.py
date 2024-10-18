from datetime import datetime

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from weatherapp_query.models import Weather
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


@pytest.fixture
def weather_object():
    return Weather(
        timestamp=datetime(2024, 1, 1),
        location_id=1,
        temperature_2m=0.01,
        relative_humidity_2m=0.02,
        dew_point_2m=0.03,
        apparent_temperature=0.04,
        pressure_msl=0.05,
        precipitation=0.06,
        rain=0.07,
        snowfall=0.08,
        cloud_cover=0.09,
        cloud_cover_low=0.10,
        cloud_cover_mid=0.11,
        cloud_cover_high=0.12,
        shortwave_radiation=0.13,
        direct_radiation=0.14,
        direct_normal_irradiance=0.15,
        diffuse_radiation=0.16,
        global_tilted_irradiance=0.17,
        sunshine_duration=0.18,
        wind_speed_10m=0.19,
        wind_speed_100m=0.20,
        wind_direction_10m=0.21,
        wind_direction_100m=0.22,
        wind_gusts_10m=0.23,
        et0_fao_evapotranspiration=0.24,
        weather_code=0,
        snow_depth=0.25,
        vapour_pressure_deficit=0.26,
    )
