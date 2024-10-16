from datetime import UTC, datetime
from decimal import Decimal

import pytest
from aiokafka import ConsumerRecord, TopicPartition
from aiosafeconsumer.datasync import EventType

from weatherapp_loader.consumers.workers import locations_worker_def
from weatherapp_loader.storage.locations import get_locations
from weatherapp_loader.types import LocationRecord


@pytest.fixture
def worker():
    return locations_worker_def.worker_class(locations_worker_def.worker_settings)


@pytest.fixture
def locations():
    return [
        LocationRecord(
            ev_time=datetime(2024, 1, 1, tzinfo=UTC),
            ev_type=EventType.REFRESH,
            ev_source="core",
            id=1,
            latitude=Decimal("1.23"),
            longitude=Decimal("4.56"),
            is_active=True,
        ),
        LocationRecord(
            ev_time=datetime(2024, 1, 1, tzinfo=UTC),
            ev_type=EventType.REFRESH,
            ev_source="core",
            id=2,
            latitude=Decimal("7.8"),
            longitude=Decimal("9.0"),
            is_active=True,
        ),
    ]


@pytest.fixture
def kafka_consumer_data(kafka_consumer_mock, locations):
    kafka_consumer_mock.getmany.return_value = {
        TopicPartition("locations", 0): [
            ConsumerRecord(
                **{
                    **{f: None for f in ConsumerRecord.__dataclass_fields__.keys()},
                    "topic": "locations",
                    "partition": 0,
                    "offset": 0,
                    "value": location,
                },
            )
            for location in locations
        ],
    }


@pytest.mark.asyncio
async def test_locations_consumer(
    storage_redis, worker, kafka_consumer_data, locations
):
    await worker.run(burst=True)

    stored_locations = await get_locations(storage_redis)
    assert stored_locations == locations
