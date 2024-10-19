import pytest
from kafkastreamer import send
from weatherapp.protocol import User as UserProto

from .utils import patch_kafka_producer

pytestmark = pytest.mark.django_db(transaction=True)


@patch_kafka_producer()
def test_user_stream(producer_m, user):
    producer_send_m = producer_m.return_value.send
    assert len(producer_send_m.mock_calls) == 0

    send([user])

    assert len(producer_send_m.mock_calls) == 1
    producer_send_call = producer_send_m.mock_calls[0]
    topic, message = producer_send_call.args

    assert topic == "users"
    data = UserProto(**message.data)
    assert data.id == user.pk
    assert data.email == user.email
    assert data.timezone == user.timezone
    assert data.temperature_unit == user.temperature_unit
    assert data.wind_speed_unit == user.wind_speed_unit
    assert data.precipitation_unit == user.precipitation_unit
    assert data.date_format == user.date_format
    assert data.time_format == user.time_format
