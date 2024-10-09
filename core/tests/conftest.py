import pytest
from ninja_jwt.tokens import RefreshToken

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
