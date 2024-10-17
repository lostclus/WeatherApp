from datetime import UTC, date, datetime
from unittest import mock

import pytest
from weatherapp.protocol.bus import EventType

from weatherapp_loader.tasks.weather import stream_weather_location_task
from weatherapp_loader.types import LocationRecord, WeatherRecord


@pytest.fixture
def weather_data():
    return [
        WeatherRecord(
            ev_time=datetime(2024, 1, 2, tzinfo=UTC),
            ev_source="loader",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
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
        ),
    ]


@pytest.fixture
def mock_get_weather(weather_data):
    async def get_weather(*args, **kwargs):
        for weather in weather_data:
            yield weather

    with mock.patch("weatherapp_loader.tasks.weather.get_weather") as get_weather_m:
        get_weather_m.side_effect = get_weather
        yield


@pytest.fixture
def kafka_producer_mock_path():
    return "weatherapp_loader.tasks.weather.AIOKafkaProducer"


@pytest.mark.asyncio
async def test_stream_weather_location_task(
    mock_get_weather, kafka_producer_mock, weather_data
):
    location = LocationRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.REFRESH,
        ev_source="core",
        id=1,
        latitude="1.23",
        longitude="4.56",
        is_active=True,
    )
    ctx = {}
    await stream_weather_location_task(
        ctx=ctx,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 1),
        location=location,
    )

    assert kafka_producer_mock.send.mock_calls == [
        mock.call("weather", weather) for weather in weather_data
    ]
