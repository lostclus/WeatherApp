import random
import string

import pytest

from weatherapp_core.users.models import User

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def password():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(8)
    )


@pytest.mark.asyncio
async def test_user_create(async_client, password):
    response = await async_client.post(
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
        "default_location_id": None,
    }

    user = await User.objects.aget(pk=user_id)
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_user_create_invalid_email(async_client, password):
    response = await async_client.post(
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
@pytest.mark.asyncio
async def test_user_create_invalid_password(pw, async_client):
    response = await async_client.post(
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


@pytest.mark.asyncio
async def test_user_create_already_exits(async_client, user, password):
    response = await async_client.post(
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
                "msg": "User already exists.",
                "loc": ["email"],
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_get(async_client, user, auth_headers):
    response = await async_client.get(
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
        "default_location_id": None,
    }


@pytest.mark.asyncio
async def test_user_get_unauthenticated(async_client, user):
    response = await async_client.get(
        f"/core/api/v1/users/{user.pk}",
        content_type="application/json",
    )

    assert response.status_code == 401, response.content


@pytest.mark.asyncio
async def test_user_get_unauthorized(async_client, user, auth_headers, other_user):
    response = await async_client.get(
        f"/core/api/v1/users/{other_user.pk}",
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 403, response.content


@pytest.mark.asyncio
async def test_user_update(async_client, user, auth_headers):
    response = await async_client.patch(
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
        "default_location_id": None,
    }


@pytest.mark.asyncio
async def test_user_update_default_location(async_client, user, auth_headers, location):
    response = await async_client.patch(
        f"/core/api/v1/users/{user.pk}",
        data={
            "default_location_id": location.pk,
        },
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
        "default_location_id": location.pk,
    }

    assert await location.aget_default_for(user)


@pytest.mark.asyncio
async def test_user_update_unauthenticated(async_client, user):
    response = await async_client.patch(
        f"/core/api/v1/users/{user.pk}",
        data={
            "date_format": "DD.MM.YYYY",
        },
        content_type="application/json",
    )

    assert response.status_code == 401, response.content


@pytest.mark.asyncio
async def test_user_update_unauthorized(async_client, user, auth_headers, other_user):
    response = await async_client.patch(
        f"/core/api/v1/users/{other_user.pk}",
        data={
            "date_format": "DD.MM.YYYY",
        },
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 403, response.content
