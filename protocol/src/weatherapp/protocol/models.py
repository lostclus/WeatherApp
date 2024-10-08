from decimal import Decimal

from pydantic import BaseModel


class City(BaseModel):
    id: int
    country_id: int
    name: str
    latitude: Decimal
    longitude: Decimal
