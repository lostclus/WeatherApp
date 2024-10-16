from datetime import UTC, datetime
from decimal import Decimal
from typing import NamedTuple

import pytest

from weatherapp.protocol.bus import EventType
from weatherapp.protocol.bus.serializers import namedtuple_to_json_serializer


class ItemRecord(NamedTuple):
    ev_time: datetime
    ev_type: EventType
    ev_source: str
    id: int
    f1: Decimal
    f2: Decimal | None
    f3: Decimal | None


@pytest.fixture
def serializer():
    return namedtuple_to_json_serializer()


def test_namedtuple_to_json_serializer(serializer):
    obj = ItemRecord(
        ev_time=datetime(2024, 1, 1, tzinfo=UTC),
        ev_type=EventType.CREATE,
        ev_source="source",
        id=1,
        f1=Decimal("1.2"),
        f2=Decimal("3.4"),
        f3=None,
    )

    payload = serializer(obj)

    assert payload == (
        b'{"_time": "2024-01-01T00:00:00+00:00", "_type": "create", "_source": "source"'
        b', "id": 1, "f1": "1.2", "f2": "3.4", "f3": null}'
    )
