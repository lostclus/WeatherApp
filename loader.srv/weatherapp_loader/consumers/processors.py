import pickle
from dataclasses import dataclass
from typing import Any

from aiosafeconsumer.datasync import EnumerateIDsRecord, EventType, ObjectID, Version
from aiosafeconsumer.datasync.redis import RedisWriter, RedisWriterSettings

from ..constants import LOCATIONS_KEY_PREFIX, LOCATIONS_VERSIONS_KEY
from ..storage.redis import get_redis
from ..types import (
    Location,
    LocationDeleteRecord,
    LocationEnumerateRecord,
    LocationRecord,
)


@dataclass
class LocationsWriterSettings(RedisWriterSettings[Location]):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            redis=get_redis,
            version_getter=self._version_getter,
            event_type_getter=self._event_type_getter,
            id_getter=self._id_getter,
            enum_getter=self._enum_getter,
            version_serializer=self._version_serializer,
            version_deserializer=self._version_deserializer,
            record_serializer=self._record_serializer,
            key_prefix=LOCATIONS_KEY_PREFIX,
            versions_key=LOCATIONS_VERSIONS_KEY,
            **kwargs,
        )

    @staticmethod
    def _version_getter(item: Location) -> Version:
        return int(item.ev_time.timestamp())

    @staticmethod
    def _record_serializer(item: Location) -> bytes:
        return pickle.dumps(item)

    @staticmethod
    def _event_type_getter(item: Location) -> EventType:
        return EventType(item.ev_type)

    @staticmethod
    def _id_getter(item: Location) -> ObjectID:
        assert isinstance(item, LocationRecord) or isinstance(
            item, LocationDeleteRecord
        )
        return item.id

    @staticmethod
    def _enum_getter(item: Location) -> EnumerateIDsRecord:
        assert isinstance(item, LocationEnumerateRecord)
        return EnumerateIDsRecord(ids=list(item.ids))

    @staticmethod
    def _version_serializer(ver: Version) -> bytes:
        return str(ver).encode()

    @staticmethod
    def _version_deserializer(val: bytes) -> Version:
        return int(val.decode())


class LocationsWriter(RedisWriter[Location]):
    pass
