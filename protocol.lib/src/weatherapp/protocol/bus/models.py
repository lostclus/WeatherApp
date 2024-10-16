from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..types import TimeZone


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    last_login: datetime | None
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime
    timezone: TimeZone
    temperature_unit: str
    wind_speed_unit: str
    precipitation_unit: str
    date_format: str
    time_format: str

    model_config = ConfigDict(extra="forbid")


class Location(BaseModel):
    id: int
    name: str
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    user_id: int | None
    is_default: bool
    is_active: bool

    model_config = ConfigDict(extra="forbid")


class Weather(BaseModel):
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
