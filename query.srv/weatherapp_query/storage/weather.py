from collections.abc import Sequence
from datetime import UTC, datetime

from ..models import Weather, WeatherDataField
from .clickhouse import ClickHouseClient, build_filters


async def get_weather(
    ch: ClickHouseClient,
    location_ids: Sequence[int],
    timestamp_start: datetime,
    timestamp_end: datetime,
    fields: Sequence[WeatherDataField] | None = None,
) -> list[Weather]:
    fields = fields or list(WeatherDataField)

    filters = {
        "location_id__in": location_ids,
        "timestamp__gte": timestamp_start,
        "timestamp__lt": timestamp_end,
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
            ORDER BY _time DESC
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
