from decimal import Decimal

from ninja import ModelSchema
from pydantic import Field

from .models import Location


class LocationInSchema(ModelSchema):
    name: str = Field(max_length=200)
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    is_default: bool = False

    class Meta:
        model = Location
        fields = [
            "name",
            "latitude",
            "longitude",
            "is_active",
        ]


class LocationOutSchema(ModelSchema):
    is_default: bool

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "user",
            "is_active",
        ]
