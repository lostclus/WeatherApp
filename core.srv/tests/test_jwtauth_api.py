import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.asyncio
async def test_token_create(async_client, user):
    user.set_password("test_password")
    await user.asave()

    response = await async_client.post(
        "/core/api/v1/token/",
        data={
            "email": user.email,
            "password": "test_password",
        },
        content_type="application/json",
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "email": user.email,
        "user_id": user.pk,
        "token_access": response_data["token_access"],
        "token_refresh": response_data["token_refresh"],
        "token_access_life_time": int(
            settings.JWT_ACCESS_TOKEN_LIFETIME.total_seconds()
        ),
    }


@pytest.mark.asyncio
async def test_token_create_invalid_password(async_client, user):
    user.set_password("test_password")
    await user.asave()

    response = await async_client.post(
        "/core/api/v1/token/",
        data={
            "email": user.email,
            "password": "invalid",
        },
        content_type="application/json",
    )

    assert response.status_code == 401, response.content


@pytest.mark.asyncio
async def test_token_refresh(async_client, user, jwt_token):
    response = await async_client.post(
        "/core/api/v1/token/refresh",
        data={
            "token_refresh": jwt_token.token_refresh,
        },
        content_type="application/json",
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "email": user.email,
        "user_id": user.pk,
        "token_access": response_data["token_access"],
        "token_refresh": response_data["token_refresh"],
        "token_access_life_time": int(
            settings.JWT_ACCESS_TOKEN_LIFETIME.total_seconds()
        ),
    }


@pytest.mark.asyncio
async def test_token_refresh_invalid_token(async_client):
    response = await async_client.post(
        "/core/api/v1/token/refresh",
        data={
            "token_refresh": "invalid",
        },
        content_type="application/json",
    )

    assert response.status_code == 401, response.content
