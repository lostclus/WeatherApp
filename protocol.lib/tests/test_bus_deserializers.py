from datetime import UTC, datetime
from decimal import Decimal
from typing import NamedTuple

import pytest

from weatherapp.protocol.bus import EventType
from weatherapp.protocol.bus.deserializers import json_to_namedtuple_deserializer


class ItemRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    id: int
    f1: Decimal
    f2: Decimal | None
    f3: Decimal | None


class ItemDeleteRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    id: int


class ItemEnumerateRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    ids: list[int]


class ItemEOSRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str


@pytest.fixture
def deserializer():
    return json_to_namedtuple_deserializer(
        ItemRecord, ItemDeleteRecord, ItemEnumerateRecord, ItemEOSRecord
    )


def test_json_to_namedtuple_deserializer_item_record(deserializer):
    payload = (
        b'{"_time":"2024-01-01T00:00:00+00:00","_type":"create","_source":"source"'
        b',"id":1,"f1":"1.2","f2":"3.4","f3":null}'
    )

    obj = deserializer(payload)
    assert obj == ItemRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.CREATE,
        ev_source="source",
        id=1,
        f1=Decimal("1.2"),
        f2=Decimal("3.4"),
        f3=None,
    )


def test_json_to_namedtuple_deserializer_item_delete_record(deserializer):
    payload = (
        b'{"_time":"2024-01-01T00:00:00+00:00","_type":"delete","_source":"source"'
        b',"id":1}'
    )

    obj = deserializer(payload)
    assert obj == ItemDeleteRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.DELETE,
        ev_source="source",
        id=1,
    )


def test_json_to_namedtuple_deserializer_item_enumerate_record(deserializer):
    payload = (
        b'{"_time":"2024-01-01T00:00:00+00:00","_type":"enumerate","_source":"source"'
        b',"ids":[1,2,3]}'
    )

    obj = deserializer(payload)
    assert obj == ItemEnumerateRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.ENUMERATE,
        ev_source="source",
        ids=[1, 2, 3],
    )


def test_json_to_namedtuple_deserializer_item_eos_record(deserializer):
    payload = b'{"_time":"2024-01-01T00:00:00+00:00","_type":"eos","_source":"source"}'

    obj = deserializer(payload)
    assert obj == ItemEOSRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.EOS,
        ev_source="source",
    )
