from datetime import UTC, datetime, timedelta

import pytest

from weatherapp_core.jwtauth.logic import create_token_for_user

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
        "token_access_expires_at": response_data["token_access_expires_at"],
    }

    assert response_data["token_access"] > ""
    assert response_data["token_refresh"] > ""

    token_access_expires_at = datetime.fromisoformat(
        response_data["token_access_expires_at"]
    )

    assert token_access_expires_at > datetime.now(UTC)


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
    response_data = response.json()

    assert response_data == {"detail": "Authentication failed"}


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
        "token_access_expires_at": response_data["token_access_expires_at"],
    }

    assert response_data["token_access"] > ""
    assert response_data["token_refresh"] > ""

    token_access_expires_at = datetime.fromisoformat(
        response_data["token_access_expires_at"]
    )

    assert token_access_expires_at > datetime.now(UTC)


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
    response_data = response.json()

    assert response_data == {"detail": "Authentication failed"}


@pytest.mark.asyncio
async def test_token_refresh_expired_token(async_client, user):
    token = create_token_for_user(user, now=datetime.now(UTC) - timedelta(days=365))
    response = await async_client.post(
        "/core/api/v1/token/refresh",
        data={
            "token_refresh": token.token_refresh,
        },
        content_type="application/json",
    )

    assert response.status_code == 401, response.content
    response_data = response.json()

    assert response_data == {"detail": "Signature has expired"}
