import pickle
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from aiosafeconsumer.datasync import EnumerateIDsRecord, EventType, ObjectID, Version
from aiosafeconsumer.datasync.redis import RedisWriter, RedisWriterSettings

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
            version_serializer=str,
            version_deserializer=int,
            record_serializer=self._record_serializer,
            **kwargs,
        )

    @staticmethod
    def _version_getter(item: Location) -> Version:
        return int(datetime.fromisoformat(item.ev_time).timestamp())

    @staticmethod
    def _record_serializer(item: Location) -> bytes:
        return pickle.dumps(item._asdict())

    @staticmethod
    def _event_type_getter(item: Location) -> EventType:
        return item.ev_type

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


class LocationsWriter(RedisWriter[Location]):
    pass
