from datetime import date
from typing import TYPE_CHECKING, Any

if not TYPE_CHECKING:
    from aiokafka import AIOKafkaProducer
else:
    from .kafka_stubs import AIOKafkaProducer

from weatherapp.protocol.bus.serializers import namedtuple_to_json_serializer

from .. import settings
from ..service.open_meteo import get_weather
from ..types import LocationRecord


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
) -> None:
    producer = _create_kafka_producer()
    try:
        await producer.start()
        async for weather in get_weather(
            start_date=start_date,
            end_date=end_date,
            location=location,
        ):
            await producer.send("weather", weather)
    finally:
        await producer.flush()
        await producer.stop()
