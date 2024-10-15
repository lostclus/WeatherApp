from decimal import Decimal

from ninja import ModelSchema
from pydantic import Field

from .models import Location


class LocationInSchema(ModelSchema):
    name: str = Field(max_length=200)
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)

    class Config:
        model = Location
        model_fields = [
            "name",
            "latitude",
            "longitude",
            "is_default",
            "is_active",
        ]


class LocationOutSchema(ModelSchema):
    class Config:
        model = Location
        model_fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "user",
            "is_default",
            "is_active",
        ]
