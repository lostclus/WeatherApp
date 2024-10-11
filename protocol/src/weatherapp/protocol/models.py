from decimal import Decimal

from pydantic import BaseModel


class Location(BaseModel):
    id: int
    name: str
    latitude: Decimal
    longitude: Decimal
    user_id: int
    is_default: bool
    is_active: bool


class User(BaseModel):
    id: int
    email: str
    timezone: str
    temperature_unit: str
    wind_speed_unit: str
    precipitation_unit: str
    date_format: str
    time_format: str
    is_active: bool
