from datetime import datetime, timedelta

import pytest
from weatherapp.protocol import (
    PrecipitationUnit,
    TemperatureUnit,
    WeatherDataField,
    WindSpeedUnit,
)

from weatherapp_query.storage.weather import add_weather


@pytest.mark.asyncio
async def test_weather(client, auth_headers, clickhouse_client, weather_object):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == [
        {
            "timestamp": "2024-01-01T00:00:00",
            "location_id": 1,
            "temperature_2m": 0.01,
            "relative_humidity_2m": 0.02,
            "dew_point_2m": 0.03,
            "apparent_temperature": 0.04,
            "pressure_msl": 0.05,
            "precipitation": 0.06,
            "rain": 0.07,
            "snowfall": 0.08,
            "cloud_cover": 0.09,
            "cloud_cover_low": 0.10,
            "cloud_cover_mid": 0.11,
            "cloud_cover_high": 0.12,
            "shortwave_radiation": 0.13,
            "direct_radiation": 0.14,
            "direct_normal_irradiance": 0.15,
            "diffuse_radiation": 0.16,
            "global_tilted_irradiance": 0.17,
            "sunshine_duration": 0.18,
            "wind_speed_10m": 0.19,
            "wind_speed_100m": 0.20,
            "wind_direction_10m": 0.21,
            "wind_direction_100m": 0.22,
            "wind_gusts_10m": 0.23,
            "et0_fao_evapotranspiration": 0.24,
            "weather_code": 0,
            "snow_depth": 0.25,
            "vapour_pressure_deficit": 0.26,
        },
    ]


@pytest.mark.asyncio
async def test_weather_timezone(
    client, auth_headers, clickhouse_client, weather_object
):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "timezone": "Europe/Kyiv",
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data[0]["timestamp"] == "2024-01-01T02:00:00"


@pytest.mark.parametrize("tz_name", ["UTC", "Europe/Kyiv"])
@pytest.mark.asyncio
async def test_weather_date_filter(
    tz_name, client, auth_headers, clickhouse_client, weather_object
):
    def gen_houry_timestamps(start, end):
        result = []
        ts = start
        while ts < end:
            result.append(ts)
            ts += timedelta(hours=1)
        return result

    insert_timestamps = gen_houry_timestamps(datetime(2024, 1, 1), datetime(2024, 1, 6))

    await add_weather(
        clickhouse_client,
        *[
            weather_object.model_copy(update={"timestamp": ts})
            for ts in insert_timestamps
        ],
    )

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-02",
        "end_date": "2024-01-03",
        "fields": ["temperature_2m"],
        "timezone": tz_name,
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    expect_timestamps = gen_houry_timestamps(datetime(2024, 1, 2), datetime(2024, 1, 4))

    response_timestamps = [
        datetime.fromisoformat(item["timestamp"]) for item in response_data
    ]

    assert response_timestamps == expect_timestamps


@pytest.mark.parametrize("field", list(WeatherDataField))
@pytest.mark.asyncio
async def test_weather_fields(
    field, client, auth_headers, clickhouse_client, weather_object
):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": [field],
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == [
        {
            "timestamp": "2024-01-01T00:00:00",
            "location_id": 1,
            field: response_data[0][field],
        },
    ]


@pytest.mark.parametrize(
    "unit,expect",
    (
        (TemperatureUnit.CELSIUS, 0.01),
        (TemperatureUnit.FAHRENHEIT, 32.018),
    ),
)
@pytest.mark.asyncio
async def test_weather_temperature_unit(
    unit, expect, client, auth_headers, clickhouse_client, weather_object
):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": ["temperature_2m"],
        "temperature_unit": str(unit),
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data[0]["temperature_2m"] == expect


@pytest.mark.parametrize(
    "unit,expect",
    (
        (WindSpeedUnit.M_S, 0.19),
        (WindSpeedUnit.KM_H, 0.684),
        (WindSpeedUnit.KNOTS, 0.369330778),
    ),
)
@pytest.mark.asyncio
async def test_weather_wind_speed_unit(
    unit, expect, client, auth_headers, clickhouse_client, weather_object
):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": ["wind_speed_10m"],
        "wind_speed_unit": str(unit),
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data[0]["wind_speed_10m"] == expect


@pytest.mark.parametrize(
    "unit,expect",
    (
        (PrecipitationUnit.MILLIMETER, 0.06),
        (PrecipitationUnit.INCH, 0.002362206),
    ),
)
@pytest.mark.asyncio
async def test_weather_precipitation_unit(
    unit, expect, client, auth_headers, clickhouse_client, weather_object
):
    await add_weather(clickhouse_client, weather_object)

    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": ["precipitation"],
        "precipitation_unit": str(unit),
    }

    response = await client.post("/weather", json=request_data, headers=auth_headers)
    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data[0]["precipitation"] == expect


@pytest.mark.asyncio
async def test_weather_unauthenticated(client):
    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": ["temperature_2m"],
    }
    response = await client.post("/weather", json=request_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_weather_invalid_token(client):
    request_data = {
        "location_ids": [1],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "fields": ["temperature_2m"],
    }
    response = await client.post(
        "/weather",
        json=request_data,
        headers={"Authorization": "Bearer invalid"},
    )
    assert response.status_code == 400
