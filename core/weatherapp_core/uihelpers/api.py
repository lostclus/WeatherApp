from typing import Any

from django.http import HttpRequest
from ninja import Router

from weatherapp_core.api_auth import async_auth
from weatherapp_core.constants import (
    DateFormatChoices,
    PrecipitationUnitChoices,
    TemperatureUnitChoices,
    TimeFormatChoices,
    TimeZoneChoices,
    WindSpeedUnitChoices,
)

from .schema import ConstantsSchema

router = Router(auth=async_auth)


@router.get("/constants")
async def constants(request: HttpRequest) -> ConstantsSchema:
    def choices_to_dict(choices: Any) -> dict[str, str]:
        return {str(value): str(text) for value, text in choices.choices}

    return ConstantsSchema(
        timezones=choices_to_dict(TimeZoneChoices),
        temperature_units=choices_to_dict(TemperatureUnitChoices),
        wind_speed_units=choices_to_dict(WindSpeedUnitChoices),
        precipitation_units=choices_to_dict(PrecipitationUnitChoices),
        date_formats=choices_to_dict(DateFormatChoices),
        time_formats=choices_to_dict(TimeFormatChoices),
    )
