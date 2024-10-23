from typing import Any

from django.http import HttpRequest
from ninja import Router
from pydantic import BaseModel
from weatherapp.protocol import WeatherData

from weatherapp_core.constants import (
    AggregateFunctionChoices,
    AggregateGroupChoices,
    DateFormatChoices,
    PrecipitationUnitChoices,
    TemperatureUnitChoices,
    TimeFormatChoices,
    TimeZoneChoices,
    WindSpeedUnitChoices,
)

from .schema import ConstantsSchema

uihelpers_router = Router()


@uihelpers_router.get("/constants")
async def constants(request: HttpRequest) -> ConstantsSchema:
    def from_choices(choices: Any) -> dict[str, str]:
        return {str(value): str(text) for value, text in choices.choices}

    def from_pydantic_model(model: type[BaseModel]) -> dict[str, str]:
        return {name: info.title or name for name, info in model.model_fields.items()}

    return ConstantsSchema(
        timezones=from_choices(TimeZoneChoices),
        temperature_units=from_choices(TemperatureUnitChoices),
        wind_speed_units=from_choices(WindSpeedUnitChoices),
        precipitation_units=from_choices(PrecipitationUnitChoices),
        date_formats=from_choices(DateFormatChoices),
        time_formats=from_choices(TimeFormatChoices),
        weather_fields=from_pydantic_model(WeatherData),
        aggregate_groups=from_choices(AggregateGroupChoices),
        aggregate_functions=from_choices(AggregateFunctionChoices),
    )
