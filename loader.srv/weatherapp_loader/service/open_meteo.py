import types
import typing
from collections.abc import AsyncGenerator
from datetime import UTC, date, datetime

import aiohttp

from ..types import LocationRecord, WeatherRecord

BASE_URL = "https://archive-api.open-meteo.com"
EV_SOURCE = "loader"


async def get_weather(
    start_date: date,
    end_date: date,
    location: LocationRecord,
    now: datetime | None = None,
) -> AsyncGenerator[WeatherRecord, None]:

    weather_fields = WeatherRecord._fields[4:]
    weather_types = WeatherRecord.__annotations__

    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        url = "/v1/archive"
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "hourly": ",".join(weather_fields),
            "wind_speed_unit": "ms",
        }
        async with session.get(url=url, params=params) as resp:
            resp_data = await resp.json()

    hourly = resp_data["hourly"]
    ev_time = now or datetime.now(UTC)

    for idx, tm in enumerate(hourly["time"]):
        timestamp = datetime.fromisoformat(tm).replace(tzinfo=UTC)

        data = {}
        for field in weather_fields:
            value = hourly[field][idx]
            if value is not None:
                f_type = weather_types[field]
                if typing.get_origin(f_type) is types.UnionType:
                    f_type = typing.get_args(f_type)[0]
                value = f_type(value)
            data[field] = value

        yield WeatherRecord(
            ev_time=ev_time,
            ev_source=EV_SOURCE,
            timestamp=timestamp,
            location_id=location.id,
            **data,
        )
