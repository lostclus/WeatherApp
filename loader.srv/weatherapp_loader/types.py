from typing import NamedTuple

from aiosafeconsumer.datasync import EventType


class LocationRecord(NamedTuple):
    ev_time: str
    ev_type: EventType
    ev_source: str
    id: int
    latitude: str
    longitude: str
    is_active: bool


class LocationDeleteRecord(NamedTuple):
    ev_time: str
    ev_type: EventType
    ev_source: str
    id: int


class LocationEnumerateRecord(NamedTuple):
    ev_time: str
    ev_type: EventType
    ev_source: str
    ids: list[int]


Location = LocationRecord | LocationDeleteRecord | LocationEnumerateRecord
