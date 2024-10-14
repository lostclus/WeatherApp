from decimal import Decimal

import pytest
import pytest_asyncio

from weatherapp_core.geo.models import Location
from weatherapp_core.jwtauth.logic import create_token_for_user
from weatherapp_core.users.models import User


@pytest_asyncio.fixture
async def user(django_db_blocker):
    with django_db_blocker.unblock():
        return await User.objects.acreate(email="test@example.com")


@pytest.fixture
def jwt_token(user):
    token = create_token_for_user(user)
    return token


@pytest.fixture
def auth_headers(jwt_token):
    return {
        "Authorization": f"Bearer {jwt_token.token_access}",
    }


@pytest_asyncio.fixture
async def other_user(django_db_blocker):
    with django_db_blocker.unblock():
        other_user = await User.objects.acreate(email="other@example.com")
        return other_user


@pytest_asyncio.fixture
async def location(django_db_blocker, user):
    with django_db_blocker.unblock():
        location = await Location.objects.acreate(
            name="Null island",
            latitude=Decimal(0),
            longitude=Decimal(0),
            user=user,
        )
        return location
