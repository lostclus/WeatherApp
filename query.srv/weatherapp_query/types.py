from datetime import UTC, datetime, timezone
from typing import Annotated, Any, TypedDict, cast

from pydantic import (
    FieldSerializationInfo,
    SerializerFunctionWrapHandler,
    WrapSerializer,
)


class SerializationContext(TypedDict):
    timezone: timezone


def _convert_timezone(
    value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo
) -> str:
    assert isinstance(value, datetime)
    context = cast(SerializationContext | None, info.context)
    if context:
        if tz := context.get("timezone"):
            if not value.tzinfo:
                value = value.replace(tzinfo=UTC)
            value = value.astimezone(tz)

    return str(nxt(value.replace(tzinfo=None)))


DateTimeConvertTZ = Annotated[
    datetime, WrapSerializer(_convert_timezone, when_used="json")
]
