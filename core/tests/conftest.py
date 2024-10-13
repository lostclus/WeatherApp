from decimal import Decimal

import pytest
from ninja_jwt.tokens import RefreshToken

from weatherapp_core.geo.models import Location
from weatherapp_core.users.models import User


@pytest.fixture
def user(django_db_blocker):
    with django_db_blocker.unblock():
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
def other_user(django_db_blocker):
    with django_db_blocker.unblock():
        other_user = User.objects.create(email="other@example.com")
        return other_user


@pytest.fixture
def location(django_db_blocker, user):
    with django_db_blocker.unblock():
        location = Location.objects.create(
            name="Null island",
            latitude=Decimal(0),
            longitude=Decimal(0),
            user=user,
        )
        return location
