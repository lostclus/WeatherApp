from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class WeatherData(BaseModel):
    temperature_2m: float | None = None
    relative_humidity_2m: float | None = None
    dew_point_2m: float | None = None
    apparent_temperature: float | None = None
    pressure_msl: float | None = None
    precipitation: float | None = None
    rain: float | None = None
    snowfall: float | None = None
    cloud_cover: float | None = None
    cloud_cover_low: float | None = None
    cloud_cover_mid: float | None = None
    cloud_cover_high: float | None = None
    shortwave_radiation: float | None = None
    direct_radiation: float | None = None
    direct_normal_irradiance: float | None = None
    diffuse_radiation: float | None = None
    global_tilted_irradiance: float | None = None
    sunshine_duration: float | None = None
    wind_speed_10m: float | None = None
    wind_speed_100m: float | None = None
    wind_direction_10m: float | None = None
    wind_direction_100m: float | None = None
    wind_gusts_10m: float | None = None
    et0_fao_evapotranspiration: float | None = None
    weather_code: int | None = None
    snow_depth: float | None = None
    vapour_pressure_deficit: float | None = None


class Weather(WeatherData):
    timestamp: datetime
    location_id: int


# This enum is for fields set validation at runtime, so that mypy don't have to
# use this
WeatherDataField = StrEnum(  # type: ignore
    "WeatherDataField", [(field, field) for field in WeatherData.model_fields.keys()]
)
