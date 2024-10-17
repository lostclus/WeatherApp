import logging
from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING, Any

if not TYPE_CHECKING:
    from aiokafka import AIOKafkaProducer
else:
    from .kafka_stubs import AIOKafkaProducer

from weatherapp.protocol.bus.serializers import namedtuple_to_json_serializer

from .. import settings
from ..service.open_meteo import get_weather
from ..storage.locations import get_locations
from ..types import LocationRecord, OpenMeteoDataset
from .arq import func_path, get_arq_pool

log = logging.getLogger(__name__)


def _create_kafka_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=namedtuple_to_json_serializer(),
    )
    return producer


async def stream_weather_location_task(
    ctx: dict[str, Any],
    start_date: date,
    end_date: date,
    location: LocationRecord,
    dataset: OpenMeteoDataset | None = None,
) -> int:
    producer = _create_kafka_producer()
    try:
        await producer.start()
        records_count = 0
        async for weather in get_weather(
            start_date=start_date,
            end_date=end_date,
            location=location,
            dataset=dataset,
        ):
            await producer.send("weather", weather)
            records_count += 1
    finally:
        await producer.flush()
        await producer.stop()

    log.info(
        f"{records_count} records was streamed for location #{location.id} and dates"
        f" {start_date}..{end_date}"
    )
    return records_count


async def stream_weather_task(
    ctx: dict[str, Any],
    start_date: date | None = None,
    end_date: date | None = None,
    location_ids: Sequence[int] | None = None,
    dataset: OpenMeteoDataset | None = None,
) -> int:
    today = datetime.now(UTC).date()
    start_date = start_date or (today - timedelta(days=3))
    end_date = end_date or today

    locations_d = {location.id: location for location in await get_locations()}
    locations: list[LocationRecord]

    if location_ids:
        locations = [locations_d[location_id] for location_id in location_ids]
    else:
        locations = [
            location for location in locations_d.values() if location.is_active
        ]

    jobs_count = 0
    async with get_arq_pool() as arq_pool:
        for location in locations:
            await arq_pool.enqueue_job(
                func_path(stream_weather_location_task),
                start_date=start_date,
                end_date=end_date,
                location=location,
                dataset=dataset,
            )
            jobs_count += 1

    return jobs_count
