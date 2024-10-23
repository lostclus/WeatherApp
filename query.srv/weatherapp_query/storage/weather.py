import itertools
from collections.abc import Sequence
from datetime import UTC, datetime

from pydantic_extra_types.timezone_name import TimeZoneName
from weatherapp.protocol import (
    AggregateFunction,
    AggregateGroup,
    WeatherDataAggregatedField,
    WeatherDataField,
)

from ..models import Weather, WeatherAggregated
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


async def get_aggregated_weather(
    ch: ClickHouseClient,
    location_ids: Sequence[int],
    timestamp_start: datetime,
    timestamp_end: datetime,
    timezone: TimeZoneName,
    group: AggregateGroup,
    fields: Sequence[WeatherDataAggregatedField] | None = None,
) -> list[WeatherAggregated]:
    fields = fields or list(WeatherDataAggregatedField)

    agg_sql_map = {
        AggregateFunction.MIN: "min({base_field})",
        AggregateFunction.MAX: "max({base_field})",
        AggregateFunction.AVG: "avg({base_field})",
        AggregateFunction.MEDIAN: "median({base_field})",
        AggregateFunction.DIFF_MAX_MIN: "(max({base_field}) - min({base_field}))",
    }

    agg_info = {
        f"{field}_{func}": (WeatherDataField(field), AggregateFunction(func))
        for field, func in itertools.product(WeatherDataField, AggregateFunction)
    }

    base_fields: set[WeatherDataField] = set()
    agg_fields: list[str] = []
    for field in fields:
        base_field, func = agg_info[field]
        expr_sql = agg_sql_map[func].format(base_field=base_field)
        field_sql = f"{expr_sql} AS {field}"
        base_fields.add(base_field)
        agg_fields.append(field_sql)
    agg_fields_sql = ",".join(agg_fields)

    group_timestamp_map = {
        AggregateGroup.DAY: "toStartOfDay({})",
        AggregateGroup.WEEK: "toStartOfWeek({}, 1)",
        AggregateGroup.MONTH: "toStartOfMonth({})",
        AggregateGroup.YEAR: "toStartOfYear({})",
    }
    timestamp_tz_sql = "toDateTime(timestamp, {timezone})"
    timestamp_agg_func_sql = group_timestamp_map[group].format(timestamp_tz_sql)
    group_timestamp_sql = f"toDateTime({timestamp_agg_func_sql}, 'UTC')"

    filters = {
        "location_id__in": location_ids,
        "timestamp__gte": timestamp_start,
        "timestamp__lt": timestamp_end,
    }

    select_fields = sorted([str(field) for field in base_fields])
    select_fields_sql = ",".join(select_fields)
    filters_sql, sql_params, _ = build_filters(filters, *Weather.model_fields.keys())

    sql_params["timezone"] = str(timezone)

    sql = f"""
        SELECT
            timestamp,
            location_id,
            {agg_fields_sql}
        FROM (
            SELECT
                {group_timestamp_sql} AS timestamp,
                location_id,
                {select_fields_sql}
            FROM (
                SELECT
                    timestamp,
                    location_id,
                    {select_fields_sql}
                FROM weather
                PREWHERE {filters_sql}
                ORDER BY _time DESC
                LIMIT 1 BY (timestamp, location_id)
            )
        )
        GROUP BY timestamp, location_id
        ORDER BY timestamp
    """

    results: list[Weather] = []
    rows = await ch.fetch(sql, params=sql_params)
    results = [WeatherAggregated(**row) for row in rows]

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
