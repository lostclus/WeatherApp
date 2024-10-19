from datetime import date, datetime, timedelta

from fastapi import APIRouter, Response
from pydantic import BaseModel, TypeAdapter
from pydantic_extra_types.timezone_name import TimeZoneName
from zoneinfo import ZoneInfo

from ..models import Weather, WeatherDataField
from ..storage.weather import get_weather
from .dependencies import ClickHouseDep

router = APIRouter()


class WeatherRequest(BaseModel):
    location_id: int
    start_date: date
    end_date: date
    fields: list[WeatherDataField] | None = None
    timezone: TimeZoneName = TimeZoneName("UTC")


@router.post("/weather", response_model=list[Weather])
async def weather(req: WeatherRequest, ch: ClickHouseDep) -> Response:
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
        location_ids=[req.location_id],
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        fields=req.fields,
    )

    adapter = TypeAdapter(list[Weather])
    data = adapter.dump_json(
        adapter.validate_python(objs),
        exclude_unset=True,
        context={"timezone": tz},
    )
    return Response(content=data, media_type="application/json")
