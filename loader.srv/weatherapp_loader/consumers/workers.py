from dataclasses import dataclass

from aiosafeconsumer import (
    ConsumerWorker,
    ConsumerWorkerSettings,
    WorkerDef,
    WorkerPoolSettings,
)
from weatherapp.protocol.bus.deserializers import json_to_namedtuple_deserializer

from .. import settings
from ..logging import configure_logging, configure_sentry
from ..types import (
    Location,
    LocationDeleteRecord,
    LocationEnumerateRecord,
    LocationRecord,
)
from .processors import LocationsWriter, LocationsWriterSettings
from .sources import LocationsSource, LocationsSourceSettings


@dataclass
class LocationsWorkerSettings(ConsumerWorkerSettings[Location]):
    pass


class LocationsWorker(ConsumerWorker):
    worker_type = "loader.sync_locations"


pool_settings = WorkerPoolSettings(
    workers=[
        WorkerDef(
            worker_class=LocationsWorker,
            worker_settings=LocationsWorkerSettings(
                source_class=LocationsSource,
                source_settings=LocationsSourceSettings(
                    topics=["locations"],
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=json_to_namedtuple_deserializer(
                        LocationRecord,
                        LocationDeleteRecord,
                        LocationEnumerateRecord,
                    ),
                ),
                processor_class=LocationsWriter,
                processor_settings=LocationsWriterSettings(
                    key_prefix="location:",
                    versions_key="locations",
                ),
            ),
        ),
    ]
)


def init() -> WorkerPoolSettings:
    configure_logging()
    configure_sentry()
    return pool_settings
