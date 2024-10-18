from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from ..models import Weather, WeatherDataField
from ..storage.weather import get_weather
from .dependencies import ClickHouseDep

router = APIRouter()


class WeatherRequest(BaseModel):
    location_id: int
    start_date: date
    end_date: date
    fields: list[WeatherDataField] | None = None


@router.post("/weather", response_model_exclude_unset=True)
async def weather(req: WeatherRequest, ch: ClickHouseDep) -> list[Weather]:
    return await get_weather(
        ch,
        location_ids=[req.location_id],
        start_date=req.start_date,
        end_date=req.end_date,
        fields=req.fields,
    )
