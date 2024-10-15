import pytest

pytestmark = pytest.mark.django_db(transaction=True)


def test_constraints_get(client, auth_headers):
    def is_valid_dict(value):
        return (
            isinstance(value, dict)
            and len(value) > 0
            and all(isinstance(k, str) for k in value.keys())
            and all(isinstance(v, str) for v in value.values())
        )

    response = client.get(
        "/core/api/v1/constants",
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert is_valid_dict(response_data["timezones"])
    assert is_valid_dict(response_data["temperature_units"])
    assert is_valid_dict(response_data["wind_speed_units"])
    assert is_valid_dict(response_data["precipitation_units"])
    assert is_valid_dict(response_data["date_formats"])
    assert is_valid_dict(response_data["time_formats"])
