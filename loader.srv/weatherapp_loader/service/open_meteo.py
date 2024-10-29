import logging
import types
import typing
from collections.abc import AsyncGenerator
from datetime import UTC, date, datetime
from json import JSONDecodeError
from urllib.parse import urlencode

import aiohttp

from ..types import LocationRecord, OpenMeteoDataset, WeatherRecord

EV_SOURCE = "loader"

ENDPOINTS = {
    OpenMeteoDataset.HISTORICAL_WEATHER_API: (
        "https://archive-api.open-meteo.com/v1/archive"
    ),
    OpenMeteoDataset.HISTORICAL_FORECAST_API: (
        "https://historical-forecast-api.open-meteo.com/v1/forecast"
    ),
}

log = logging.getLogger(__name__)


async def get_weather(
    start_date: date,
    end_date: date,
    location: LocationRecord,
    dataset: OpenMeteoDataset | None = None,
    now: datetime | None = None,
) -> AsyncGenerator[WeatherRecord, None]:
    dataset = dataset or OpenMeteoDataset.HISTORICAL_FORECAST_API
    weather_fields = WeatherRecord._fields[4:]
    weather_types = WeatherRecord.__annotations__

    async with aiohttp.ClientSession() as session:
        url = ENDPOINTS[dataset]
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "hourly": ",".join(weather_fields),
            "wind_speed_unit": "ms",
        }
        log.debug(f"Do request: {url}?{urlencode(params)}")
        async with session.get(url=url, params=params) as resp:
            if not resp.ok:
                text = await resp.text()
                log.error(f"OpenMeteo API error: status {resp.status}: {text}")
                resp.raise_for_status()
            try:
                resp_data = await resp.json()
            except JSONDecodeError as error:
                text = await resp.text()
                log.error(f"OpenMeteo API JSON error: {error}: {text}")
                raise

    hourly = resp_data["hourly"]
    ev_time = now or datetime.now(UTC).replace(microsecond=0)

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
