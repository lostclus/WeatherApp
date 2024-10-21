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
    is_active: bool

    model_config = ConfigDict(extra="forbid")


class WeatherData(BaseModel):
    temperature_2m: float | None = Field(
        title="Temperature (2 m)",
        default=None,
    )
    relative_humidity_2m: float | None = Field(
        title="Relative Humidity (2 m)",
        default=None,
    )
    dew_point_2m: float | None = Field(
        title="Dewpoint (2 m)",
        default=None,
    )
    apparent_temperature: float | None = Field(
        title="Apparent Temperature",
        default=None,
    )
    pressure_msl: float | None = Field(
        title="Sealevel Pressure",
        default=None,
    )
    precipitation: float | None = Field(
        title="Precipitation (rain + showers + snow)",
        default=None,
    )
    rain: float | None = Field(
        title="Rain",
        default=None,
    )
    snowfall: float | None = Field(
        title="Snowfall",
        default=None,
    )
    cloud_cover: float | None = Field(
        title="Cloud cover Total",
        default=None,
    )
    cloud_cover_low: float | None = Field(
        title="Cloud cover Low",
        default=None,
    )
    cloud_cover_mid: float | None = Field(
        title="Cloud cover Mid",
        default=None,
    )
    cloud_cover_high: float | None = Field(
        title="Cloud cover High",
        default=None,
    )
    shortwave_radiation: float | None = Field(
        title="Shortwave Solar Radiation GHI",
        default=None,
    )
    direct_radiation: float | None = Field(
        title="Direct Solar Radiation",
        default=None,
    )
    direct_normal_irradiance: float | None = Field(
        title="Direct Normal Irradiance DNI",
        default=None,
    )
    diffuse_radiation: float | None = Field(
        title="Diffuse Solar Radiation DHI",
        default=None,
    )
    global_tilted_irradiance: float | None = Field(
        title="Global Tilted Radiation GTI",
        default=None,
    )
    sunshine_duration: float | None = Field(
        title="Sunshine Duration",
        default=None,
    )
    wind_speed_10m: float | None = Field(
        title="Wind Speed (10 m)",
        default=None,
    )
    wind_speed_100m: float | None = Field(
        # TODO: check that this is valid field for both historic and forecast
        # datasets
        title="Wind Speed (100 m)",
        default=None,
    )
    wind_direction_10m: float | None = Field(
        title="Wind Direction (10 m)",
        default=None,
    )
    wind_direction_100m: float | None = Field(
        # TODO: check that this is valid field for both historic and forecast
        # datasets
        title="Wind Direction (100 m)",
        default=None,
    )
    wind_gusts_10m: float | None = Field(
        title="Wind Gusts (10 m)",
        default=None,
    )
    et0_fao_evapotranspiration: float | None = Field(
        title="Reference Evapotranspiration (ET₀)",
        default=None,
    )
    weather_code: int | None = Field(
        title="Weather code",
        default=None,
    )
    snow_depth: float | None = Field(
        title="Snow Depth",
        default=None,
    )
    vapour_pressure_deficit: float | None = Field(
        title="Vapour Pressure Deficit",
        default=None,
    )

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
