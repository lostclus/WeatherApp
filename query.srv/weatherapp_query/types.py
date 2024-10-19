from datetime import UTC, datetime, timezone
from typing import Annotated, Any, TypedDict, cast

from pydantic import (
    FieldSerializationInfo,
    SerializerFunctionWrapHandler,
    WrapSerializer,
)
from weatherapp.protocol import PrecipitationUnit, TemperatureUnit, WindSpeedUnit

from .units import decode_precipitation, decode_speed, decode_temperature


class SerializationContext(TypedDict):
    timezone: timezone
    temperature_unit: TemperatureUnit
    wind_speed_unit: WindSpeedUnit
    precipitation_unit: PrecipitationUnit


def _convert_timezone(
    value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo
) -> str:
    assert isinstance(value, datetime)
    if context := cast(SerializationContext | None, info.context):
        if tz := context.get("timezone"):
            if not value.tzinfo:
                value = value.replace(tzinfo=UTC)
            value = value.astimezone(tz)

    return str(nxt(value.replace(tzinfo=None)))


DateTime = Annotated[datetime, WrapSerializer(_convert_timezone, when_used="json")]


def _convert_temperature(
    value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo
) -> Any:
    assert type(value) is float
    if context := cast(SerializationContext | None, info.context):
        if unit := context.get("temperature_unit"):
            value = decode_temperature(value, unit)

    return nxt(value)


Temperature = Annotated[float, WrapSerializer(_convert_temperature, when_used="json")]


def _convert_wind_speed(
    value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo
) -> Any:
    assert type(value) is float
    if context := cast(SerializationContext | None, info.context):
        if unit := context.get("wind_speed_unit"):
            value = decode_speed(value, unit)

    return nxt(value)


WindSpeed = Annotated[float, WrapSerializer(_convert_wind_speed, when_used="json")]


def _convert_precipitation(
    value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo
) -> Any:
    assert type(value) is float
    if context := cast(SerializationContext | None, info.context):
        if unit := context.get("precipitation_unit"):
            value = decode_precipitation(value, unit)

    return nxt(value)


Precipitation = Annotated[
    float, WrapSerializer(_convert_precipitation, when_used="json")
]
