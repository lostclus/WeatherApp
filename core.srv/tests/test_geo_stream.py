import pytest
from kafkastreamer import send
from weatherapp.protocol import Location as LocationProto

from .utils import patch_kafka_producer

pytestmark = pytest.mark.django_db(transaction=True)


@patch_kafka_producer()
def test_location_stream(producer_m, location):
    producer_send_m = producer_m.return_value.send
    assert len(producer_send_m.mock_calls) == 0

    send([location])

    assert len(producer_send_m.mock_calls) == 1
    producer_send_call = producer_send_m.mock_calls[0]
    topic, message = producer_send_call.args

    assert topic == "locations"
    data = LocationProto(**message.data)
    assert data.id == location.pk
    assert data.name == location.name
    assert data.latitude == location.latitude
    assert data.longitude == location.longitude
    assert data.user_id == location.user_id
