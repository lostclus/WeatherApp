from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from ..types import TimeZone


class Location(BaseModel):
    id: int
    name: str
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    user_id: int | None
    is_default: bool
    is_active: bool


class User(BaseModel):
    id: int
    email: EmailStr
    timezone: TimeZone
    temperature_unit: str
    wind_speed_unit: str
    precipitation_unit: str
    date_format: str
    time_format: str
    is_active: bool
