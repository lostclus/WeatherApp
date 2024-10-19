from datetime import timedelta

import pytest

from weatherapp_query.storage.weather import add_weather, get_weather


@pytest.mark.asyncio
async def test_get_weather(clickhouse_client, weather_object):
    await add_weather(clickhouse_client, weather_object)

    objs = await get_weather(
        clickhouse_client,
        location_ids=[weather_object.location_id],
        timestamp_start=weather_object.timestamp,
        timestamp_end=weather_object.timestamp + timedelta(seconds=1),
    )

    assert objs == [weather_object]
