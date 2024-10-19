from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

if not TYPE_CHECKING:
    from aiochclient import ChClient as ClickHouseClient
else:
    from weatherapp.stubs.clickhouse import ChClient as ClickHouseClient

from aiohttp import ClientSession

from ..settings import settings

__all__ = [
    "ClickHouseClient",
    "get_clickhouse_client",
    "build_filters",
]


@asynccontextmanager
async def get_clickhouse_client(
    database: str | None = None,
) -> AsyncIterator[ClickHouseClient]:
    async with ClientSession() as session:
        client = ClickHouseClient(
            session,
            url=settings.clickhouse_url,
            database=database or settings.clickhouse_database,
            user=settings.clickhouse_user,
            password=settings.clickhouse_password,
            date_time_input_format="best_effort",
        )
        yield client


def encode_boolean(value: bool | None) -> int:
    if value is None:
        return -1
    return int(value)


def encode_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo:
        value = value.astimezone(UTC).replace(tzinfo=None)
    return value


def build_filters(
    filters: dict[str, Any],
    *fields: str,
    ignore_filters: Sequence[str] | None = None,
    coerce_dict: dict[str, Callable[[Any], Any]] | None = None,
    param_prefix: str = "",
) -> tuple[str, dict[str, Any], set[str]]:
    def encode_value(field: str, value: Any) -> Any:
        assert coerce_dict is not None
        func = coerce_dict.get(field)
        if func is not None:
            value = func(value)
        elif type(value) is bool:
            value = encode_boolean(value)
        elif isinstance(value, datetime):
            value = encode_datetime(value)
        return value

    ignore_filters = ignore_filters or []
    coerce_dict = coerce_dict or {}
    sql_filters: list[str] = []
    sql_params: dict[str, Any] = {}
    accepted_filters: set[str] = set()
    used_fields: set[str] = set()

    for field in fields:
        if field in filters:
            value = filters[field]
            sql_filters.append(f"{field} = {{{param_prefix}{field}}}")
            sql_params[f"{param_prefix}{field}"] = encode_value(field, value)
            accepted_filters.add(field)
            used_fields.add(field)
        if (filt := f"{field}__lt") in filters:
            value = filters[filt]
            sql_filters.append(f"{field} < {{{param_prefix}{filt}}}")
            sql_params[f"{param_prefix}{filt}"] = encode_value(field, value)
            accepted_filters.add(filt)
            used_fields.add(field)
        if (filt := f"{field}__lte") in filters:
            value = filters[filt]
            sql_filters.append(f"{field} <= {{{param_prefix}{filt}}}")
            sql_params[f"{param_prefix}{filt}"] = encode_value(field, value)
            accepted_filters.add(filt)
            used_fields.add(field)
        if (filt := f"{field}__gt") in filters:
            value = filters[filt]
            sql_filters.append(f"{field} > {{{param_prefix}{filt}}}")
            sql_params[f"{param_prefix}{filt}"] = encode_value(field, value)
            accepted_filters.add(filt)
            used_fields.add(field)
        if (filt := f"{field}__gte") in filters:
            value = filters[filt]
            sql_filters.append(f"{field} >= {{{param_prefix}{filt}}}")
            sql_params[f"{param_prefix}{filt}"] = encode_value(field, value)
            accepted_filters.add(filt)
            used_fields.add(field)
        if (filt := f"{field}__in") in filters:
            value = filters[filt]
            if value is not None:
                if value:
                    sql_filters.append(f"{field} IN {{{param_prefix}{filt}}}")
                    sql_params[f"{param_prefix}{filt}"] = tuple(
                        encode_value(field, x) for x in value
                    )
                else:
                    sql_filters.append("(0)")
                used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__not_in") in filters:
            value = filters[filt]
            if value is not None:
                if value:
                    sql_filters.append(f"{field} NOT IN {{{param_prefix}{filt}}}")
                    sql_params[f"{param_prefix}{filt}"] = tuple(
                        encode_value(field, x) for x in value
                    )
                    used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__overlap") in filters:
            value = filters[filt]
            if value is not None:
                if value:
                    sql_filters.append(f"hasAny({field}, {{{param_prefix}{filt}}})")
                    sql_params[f"{param_prefix}{filt}"] = list(
                        encode_value(field, x) for x in value
                    )
                else:
                    sql_filters.append("(0)")
                used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__contains") in filters:
            value = filters[filt]
            if value is not None:
                if value:
                    sql_filters.append(f"hasAll({field}, {{{param_prefix}{filt}}})")
                    sql_params[f"{param_prefix}{filt}"] = list(
                        encode_value(field, x) for x in value
                    )
                else:
                    sql_filters.append("(0)")
                used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__overlap_bits") in filters:
            value = filters[filt]
            if value is not None:
                sql_filters.append(f"bitAnd({field}, {{{param_prefix}{filt}}}) != 0")
                sql_params[f"{param_prefix}{filt}"] = value
                used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__contains_bits") in filters:
            value = filters[filt]
            if value is not None:
                sql_filters.append(
                    f"bitAnd({field}, {{{param_prefix}{filt}}})"
                    f" = %({param_prefix}{filt})s"
                )
                sql_params[f"{param_prefix}{filt}"] = value
                used_fields.add(field)
            accepted_filters.add(filt)
        if (filt := f"{field}__modulo") in filters:
            value, divider = filters[filt]
            sql_filters.append(
                f"{field} %% %({filt}_divider)s = {{{param_prefix}{filt}}}"
            )
            sql_params[f"{param_prefix}{filt}"] = value
            sql_params[f"{param_prefix}{filt}_divider"] = divider
            accepted_filters.add(filt)
            used_fields.add(field)

    invalid_filters = set(filters.keys()) - accepted_filters - set(ignore_filters or [])
    if invalid_filters:
        invalid_str = ", ".join(sorted(invalid_filters))
        raise ValueError(f"Invalid filters: {invalid_str}")

    sql = " AND ".join(sql_filters) or "(1)"
    return (sql, sql_params, used_fields)
