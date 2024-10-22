from decimal import Decimal

import pytest
import pytest_asyncio
from weatherapp.jwtauth import UserInfo

from weatherapp_core.geo.models import Location
from weatherapp_core.jwtauth.auth import get_authenticator
from weatherapp_core.users.models import User


@pytest.fixture(autouse=True)
def _override_settings(settings):
    settings.KAFKA_STREAMER["BOOTSTRAP_SERVERS"] = []


@pytest_asyncio.fixture
async def user(django_db_blocker):
    with django_db_blocker.unblock():
        return await User.objects.acreate(email="test@example.com")


@pytest.fixture
def authenticator():
    return get_authenticator()


@pytest.fixture
def jwt_token(user, authenticator):
    token = authenticator.create_token_for_user(UserInfo(user_id=user.pk))
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
