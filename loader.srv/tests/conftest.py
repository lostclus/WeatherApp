from unittest import mock

import pytest
import pytest_asyncio

from weatherapp_loader.storage.redis import close_redis_pool, get_redis, get_redis_pool


@pytest_asyncio.fixture
async def storage_redis_pool():
    pool = get_redis_pool()
    try:
        yield pool
    finally:
        redis = get_redis(pool)
        await redis.flushdb()
        await close_redis_pool()


@pytest.fixture
def storage_redis(storage_redis_pool):
    return get_redis(storage_redis_pool)


@pytest.fixture
def kafka_consumer_mock():
    with mock.patch("aiosafeconsumer.kafka.AIOKafkaConsumer") as consumer_class_m:
        consumer_m = consumer_class_m.return_value
        consumer_m.start = mock.AsyncMock()
        consumer_m.stop = mock.AsyncMock()
        consumer_m.getmany = mock.AsyncMock()
        consumer_m.commit = mock.AsyncMock()
        consumer_m._coordinator = mock.AsyncMock()

        yield consumer_m


@pytest.fixture
def kafka_producer_mock_path():
    return "aiokafka.AIOKafkaProducer"


@pytest.fixture
def kafka_producer_mock(kafka_producer_mock_path):
    with mock.patch(kafka_producer_mock_path) as producer_class_m:
        producer_m = producer_class_m.return_value
        producer_m.start = mock.AsyncMock()
        producer_m.stop = mock.AsyncMock()
        producer_m.send = mock.AsyncMock()
        producer_m.flush = mock.AsyncMock()

        yield producer_m
