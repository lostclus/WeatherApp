from datetime import UTC, datetime

import pytest

from weatherapp_query.storage.weather import add_weather


@pytest.mark.asyncio
async def test_current_weather(client, clickhouse_client, weather_object):
    now = datetime.now(UTC).replace(tzinfo=None)
    weather_object.timestamp = now.replace(minute=0, second=0, microsecond=0)

    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "fields": ["temperature_2m"],
    }

    response = await client.post("/current-weather", json=request_data)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == [
        {
            "timestamp": weather_object.timestamp.isoformat(),
            "location_id": 1,
            "temperature_2m": 0.01,
        },
    ]
