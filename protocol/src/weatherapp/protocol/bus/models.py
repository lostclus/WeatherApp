from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..types import TimeZone


class Location(BaseModel):
    id: int
    name: str
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    user_id: int | None
    is_default: bool
    is_active: bool

    model_config = ConfigDict(extra="forbid")


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
