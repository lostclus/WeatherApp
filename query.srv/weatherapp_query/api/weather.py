from datetime import UTC, date, datetime, timedelta
from typing import TypeVar
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Response
from pydantic import BaseModel, TypeAdapter
from pydantic_extra_types.timezone_name import TimeZoneName
from weatherapp.protocol import (
    AggregateGroup,
    PrecipitationUnit,
    TemperatureUnit,
    WeatherDataAggregatedField,
    WeatherDataField,
    WindSpeedUnit,
)

from ..models import Weather, WeatherAggregated
from ..storage.weather import get_aggregated_weather, get_weather
from .dependencies import AuthDep, ClickHouseDep

router = APIRouter()


class BaseLocationRequest(BaseModel):
    location_ids: list[int]


class BaseDateRangeRequest(BaseModel):
    start_date: date
    end_date: date


class BaseWeatherDataFieldsRequest(BaseModel):
    fields: list[WeatherDataField] | None = None


class BaseUnitsRequest(BaseModel):
    timezone: TimeZoneName = TimeZoneName("UTC")
    temperature_unit: TemperatureUnit = TemperatureUnit.CELSIUS
    wind_speed_unit: WindSpeedUnit = WindSpeedUnit.M_S
    precipitation_unit: PrecipitationUnit = PrecipitationUnit.MILLIMETER


class BaseWeatherRequest(BaseModel):
    location_ids: list[int]
    fields: list[WeatherDataField] | None = None
    timezone: TimeZoneName = TimeZoneName("UTC")
    temperature_unit: TemperatureUnit = TemperatureUnit.CELSIUS
    wind_speed_unit: WindSpeedUnit = WindSpeedUnit.M_S
    precipitation_unit: PrecipitationUnit = PrecipitationUnit.MILLIMETER


class WeatherRequest(
    BaseLocationRequest,
    BaseDateRangeRequest,
    BaseWeatherDataFieldsRequest,
    BaseUnitsRequest,
):
    pass


class BaseWeatherAggregatedRequest(BaseModel):
    group: AggregateGroup
    fields: list[WeatherDataAggregatedField] | None = None


class WeatherAggregatedRequest(
    BaseLocationRequest,
    BaseDateRangeRequest,
    BaseWeatherAggregatedRequest,
    BaseUnitsRequest,
):
    pass


class CurrentWeatherRequest(
    BaseLocationRequest,
    BaseWeatherDataFieldsRequest,
    BaseUnitsRequest,
):
    pass


WeatherT = TypeVar("WeatherT", bound=BaseModel)


def _serialize_weather(req: BaseUnitsRequest, objs: list[WeatherT]) -> bytes:
    tz = ZoneInfo(req.timezone)
    adapter = TypeAdapter(list[WeatherT])
    data = adapter.dump_json(
        adapter.validate_python(objs),
        exclude_unset=True,
        context={
            "timezone": tz,
            "temperature_unit": req.temperature_unit,
            "wind_speed_unit": req.wind_speed_unit,
            "precipitation_unit": req.precipitation_unit,
        },
    )
    return data


@router.post("/weather", response_model=list[Weather])
async def weather(
    req: WeatherRequest, ch: ClickHouseDep, credentials: AuthDep
) -> Response:
    tz = ZoneInfo(req.timezone)
    timestamp_start = datetime(
        req.start_date.year,
        req.start_date.month,
        req.start_date.day,
        tzinfo=tz,
    )
    timestamp_end = datetime(
        req.end_date.year,
        req.end_date.month,
        req.end_date.day,
        tzinfo=tz,
    ) + timedelta(days=1)

    objs = await get_weather(
        ch,
        location_ids=req.location_ids,
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        fields=req.fields,
    )

    content = _serialize_weather(req, objs)
    return Response(content=content, media_type="application/json")


@router.post("/current-weather", response_model=list[Weather])
async def current_weather(
    req: CurrentWeatherRequest, ch: ClickHouseDep, credentials: AuthDep
) -> Response:
    now = datetime.now(UTC).replace(microsecond=0)
    objs = await get_weather(
        ch,
        location_ids=req.location_ids,
        timestamp_start=now - timedelta(days=1),
        timestamp_end=now,
        fields=req.fields,
    )

    now_naive = now.replace(tzinfo=None)
    obj_by_loc: dict[int, Weather] = {}
    for obj in objs:
        if obj.timestamp > now_naive:
            continue
        cur_obj = obj_by_loc.get(obj.location_id)
        if cur_obj is None:
            obj_by_loc[obj.location_id] = obj
            continue
        if obj.timestamp > cur_obj.timestamp:
            obj_by_loc[obj.location_id] = obj

    content = _serialize_weather(req, list(obj_by_loc.values()))
    return Response(content=content, media_type="application/json")


@router.post("/weather-aggregated", response_model=list[WeatherAggregated])
async def weather_aggregated(
    req: WeatherAggregatedRequest, ch: ClickHouseDep, credentials: AuthDep
) -> Response:
    tz = ZoneInfo(req.timezone)
    timestamp_start = datetime(
        req.start_date.year,
        req.start_date.month,
        req.start_date.day,
        tzinfo=tz,
    )
    timestamp_end = datetime(
        req.end_date.year,
        req.end_date.month,
        req.end_date.day,
        tzinfo=tz,
    ) + timedelta(days=1)

    objs = await get_aggregated_weather(
        ch,
        location_ids=req.location_ids,
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        timezone=req.timezone,
        group=req.group,
        fields=req.fields,
    )

    content = _serialize_weather(req, objs)
    return Response(content=content, media_type="application/json")
