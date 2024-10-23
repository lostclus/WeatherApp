from datetime import datetime, timedelta

import pytest
from weatherapp.protocol import AggregateFunction, AggregateGroup

from weatherapp_query.storage.weather import add_weather


@pytest.fixture
def weather_dataset(weather_object):
    return [
        weather_object.model_copy(
            update={
                "timestamp": datetime(2024, 1, 1) + timedelta(hours=i),
                "temperature_2m": float(i),
            },
        )
        for i in range(3 * 24)
    ]


@pytest.mark.parametrize(
    "group,func,expect",
    [
        (AggregateGroup.DAY, AggregateFunction.MIN, [0.0, 24.0, 48.0]),
        (AggregateGroup.DAY, AggregateFunction.MAX, [23.0, 47.0, 71.0]),
        (AggregateGroup.DAY, AggregateFunction.AVG, [11.5, 35.5, 59.5]),
        (AggregateGroup.DAY, AggregateFunction.MEDIAN, [11.5, 35.5, 59.5]),
        (AggregateGroup.DAY, AggregateFunction.DIFF_MAX_MIN, [23.0, 23.0, 23.0]),
        (AggregateGroup.WEEK, AggregateFunction.MIN, [0.0]),
        (AggregateGroup.WEEK, AggregateFunction.MAX, [71.0]),
        (AggregateGroup.WEEK, AggregateFunction.AVG, [35.5]),
        (AggregateGroup.WEEK, AggregateFunction.MEDIAN, [35.5]),
        (AggregateGroup.WEEK, AggregateFunction.DIFF_MAX_MIN, [71.0]),
    ],
)
@pytest.mark.asyncio
async def test_weather_aggregated(
    group, func, expect, client, auth_headers, clickhouse_client, weather_dataset
):
    await add_weather(clickhouse_client, *weather_dataset)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2025-01-01",
        "group": group,
        "fields": [f"temperature_2m_{func}"],
    }

    response = await client.post(
        "/weather-aggregated", json=request_data, headers=auth_headers
    )
    assert response.status_code == 200, response.content
    response_data = response.json()

    values = [data[f"temperature_2m_{func}"] for data in response_data]

    assert values == expect
