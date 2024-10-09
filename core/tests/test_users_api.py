import random
import string

import pytest
from ninja_jwt.tokens import RefreshToken

from weatherapp_core.users.models import User


@pytest.fixture
def user():
    return User.objects.create(email="test@example.com")


@pytest.fixture
def token(user):
    return RefreshToken.for_user(user)


@pytest.fixture
def auth_headers(token):
    return {
        "Authorization": f"Bearer {token.access_token}",
    }


@pytest.fixture
def password():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(8)
    )


@pytest.mark.django_db(transaction=True)
def test_user_create(client, password):
    response = client.post(
        "/core/api/v1/users/",
        data={
            "email": "test@example.com",
            "password": password,
        },
        content_type="application/json",
    )

    assert response.status_code == 201, response.content
    response_data = response.json()

    user_id = response_data["id"]

    assert response_data == {
        "id": user_id,
        "email": "test@example.com",
        "date_format": "YYYY-MM-DD",
        "precipitation_unit": "millimeter",
        "temperature_unit": "celsius",
        "time_format": "HH:mm",
        "timezone": "UTC",
        "wind_speed_unit": "m/s",
    }

    user = User.objects.get(pk=user_id)
    assert user.email == "test@example.com"


@pytest.mark.django_db(transaction=True)
def test_user_create_invalid_email(client, password):
    response = client.post(
        "/core/api/v1/users/",
        data={
            "email": "invalid",
            "password": password,
        },
        content_type="application/json",
    )

    assert response.status_code == 422, response.content
    response_data = response.json()

    assert response_data == {
        "detail": [
            {
                "ctx": {
                    "reason": "An email address must have an @-sign.",
                },
                "loc": [
                    "body",
                    "payload",
                    "email",
                ],
                "msg": (
                    "value is not a valid email address: An email address must have an "
                    "@-sign."
                ),
                "type": "value_error",
            },
        ],
    }


@pytest.mark.parametrize("pw", ["", "1", "a", "test"])
@pytest.mark.django_db(transaction=True)
def test_user_create_invalid_password(pw, client):
    response = client.post(
        "/core/api/v1/users/",
        data={
            "email": "test@example.com",
            "password": pw,
        },
        content_type="application/json",
    )

    assert response.status_code == 422, response.content
    response_data = response.json()

    assert response_data["detail"][0]["loc"] == ["body", "payload", "password"]


@pytest.mark.django_db(transaction=True)
def test_user_create_already_exits(client, user, password):
    response = client.post(
        "/core/api/v1/users/",
        data={
            "email": user.email,
            "password": password,
        },
        content_type="application/json",
    )

    assert response.status_code == 422, response.content
    response_data = response.json()

    assert response_data == {
        "detail": [
            {
                "email": "User already exists.",
            },
        ],
    }


@pytest.mark.django_db(transaction=True)
def test_user_get(client, user, auth_headers):
    response = client.get(
        f"/core/api/v1/users/{user.pk}",
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "id": user.pk,
        "email": "test@example.com",
        "date_format": "YYYY-MM-DD",
        "precipitation_unit": "millimeter",
        "temperature_unit": "celsius",
        "time_format": "HH:mm",
        "timezone": "UTC",
        "wind_speed_unit": "m/s",
    }


@pytest.mark.django_db(transaction=True)
def test_user_get_unauthenticated(client, user):
    response = client.get(
        f"/core/api/v1/users/{user.pk}",
        content_type="application/json",
    )

    assert response.status_code == 401, response.content


@pytest.mark.django_db(transaction=True)
def test_user_update(client, user, auth_headers):
    response = client.patch(
        f"/core/api/v1/users/{user.pk}",
        data={
            "date_format": "DD.MM.YYYY",
        },
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "id": user.pk,
        "email": "test@example.com",
        "date_format": "DD.MM.YYYY",
        "precipitation_unit": "millimeter",
        "temperature_unit": "celsius",
        "time_format": "HH:mm",
        "timezone": "UTC",
        "wind_speed_unit": "m/s",
    }


@pytest.mark.django_db(transaction=True)
def test_user_update_unauthenticated(client, user):
    response = client.patch(
        f"/core/api/v1/users/{user.pk}",
        data={
            "date_format": "DD.MM.YYYY",
        },
        content_type="application/json",
    )

    assert response.status_code == 401, response.content
