import time

import jwt
import pytest
from django.conf import settings

from weatherapp_core.jwtauth.logic import (
    create_token_for_user,
    decode_token,
    encode_token,
)
from weatherapp_core.jwtauth.schema import TokenPayload, TokenType

pytestmark = pytest.mark.django_db(transaction=True)


def test_encode_decode_token():
    now = int(time.time())
    payload = TokenPayload(
        iat=now,
        exp=now + 60,
        token_type=TokenType.ACCESS,
        user_id=1,
    )
    token = encode_token(payload)

    assert token > ""

    payload2 = decode_token(token)

    assert payload2 == payload


@pytest.mark.asyncio
async def test_create_token_for_user(user):
    token = create_token_for_user(user)

    assert token.email == user.email
    assert token.user_id == user.pk

    payload = jwt.decode(
        token.token_access, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    assert payload["user_id"] == user.pk
