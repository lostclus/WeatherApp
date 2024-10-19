from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.timezone_name import TimeZoneName


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
    timezone: TimeZoneName
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

    model_config = ConfigDict(extra="forbid")


class Weather(WeatherData):
    timestamp: datetime
    location_id: int

    model_config = ConfigDict(extra="forbid")


# This enum is for fields set validation at runtime, so that mypy don't have to
# use this
WeatherDataField = StrEnum(  # type: ignore
    "WeatherDataField", [(field, field) for field in WeatherData.model_fields.keys()]
)
