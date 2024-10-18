from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta

from ..models import Weather, WeatherDataField
from .clickhouse import ClickHouseClient, build_filters


async def get_weather(
    ch: ClickHouseClient,
    location_ids: Sequence[int],
    start_date: date,
    end_date: date,
    fields: Sequence[WeatherDataField] | None = None,
) -> list[Weather]:
    start_dt = datetime(start_date.year, start_date.month, start_date.day)
    end_dt = datetime(end_date.year, end_date.month, end_date.day)
    fields = fields or list(WeatherDataField)

    filters = {
        "location_id__in": location_ids,
        "timestamp__gte": start_dt,
        "timestamp__lt": end_dt + timedelta(days=1),
    }

    all_fields = set(Weather.model_fields.keys())
    select_fields = sorted(
        [str(field) for field in fields] + ["timestamp", "location_id"]
    )
    select_fields_sql = ",".join(select_fields)
    filters_sql, sql_params, _ = build_filters(filters, *all_fields)

    sql = f"""
        SELECT *
        FROM (
            SELECT {select_fields_sql} FROM weather
            PREWHERE {filters_sql}
            LIMIT 1 BY (timestamp, location_id)
        )
        ORDER BY timestamp
    """

    results: list[Weather] = []
    rows = await ch.fetch(sql, params=sql_params)
    results = [Weather(**row) for row in rows]

    return results


async def add_weather(
    ch: ClickHouseClient, *objs: Weather, now: datetime | None = None
) -> None:
    now = now or datetime.now(UTC).replace(microsecond=0, tzinfo=None)
    fields = sorted(Weather.model_fields.keys())
    fields_sql = ",".join(fields)
    sql = f"INSERT INTO weather (_time,{fields_sql}) VALUES"
    rows = [(now,) + tuple(getattr(obj, field) for field in fields) for obj in objs]
    await ch.execute(sql, *rows)
