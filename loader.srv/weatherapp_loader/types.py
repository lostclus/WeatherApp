from datetime import datetime
from typing import NamedTuple

from weatherapp.protocol.bus import EventType


class LocationRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    id: int
    latitude: str
    longitude: str
    is_active: bool


class LocationDeleteRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    id: int


class LocationEnumerateRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    ids: list[int]


Location = LocationRecord | LocationDeleteRecord | LocationEnumerateRecord


class WeatherRecord(NamedTuple):
    ev_time: datetime
    ev_source: str
    timestamp: datetime
    location_id: int
    temperature_2m: float | None
    relative_humidity_2m: float | None
    dew_point_2m: float | None
    apparent_temperature: float | None
    pressure_msl: float | None
    precipitation: float | None
    rain: float | None
    snowfall: float | None
    cloud_cover: float | None
    cloud_cover_low: float | None
    cloud_cover_mid: float | None
    cloud_cover_high: float | None
    shortwave_radiation: float | None
    direct_radiation: float | None
    direct_normal_irradiance: float | None
    diffuse_radiation: float | None
    global_tilted_irradiance: float | None
    sunshine_duration: float | None
    wind_speed_10m: float | None
    wind_speed_100m: float | None
    wind_direction_10m: float | None
    wind_direction_100m: float | None
    wind_gusts_10m: float | None
    et0_fao_evapotranspiration: float | None
    weather_code: int | None
    snow_depth: float | None
    vapour_pressure_deficit: float | None
