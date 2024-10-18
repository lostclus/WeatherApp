from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from ..models import Weather
from .dependencies import ClickHouseDep


class WeatherRequest(BaseModel):
    location: int
    start_date: datetime
    end_date: datetime


router = APIRouter()


@router.get("/query/api/v1/weather")
async def weather(payload: WeatherRequest, ch: ClickHouseDep) -> list[Weather]:
    sql = """
        SELECT *
        FROM (
            SELECT * FROM weather
            LIMIT 1 BY (timestamp, location_id)
        )
        ORDER BY timestamp
    """
    results = await ch.execute(sql)
    print("***", results)
    return []
