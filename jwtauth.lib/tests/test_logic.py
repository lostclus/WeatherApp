from datetime import UTC, datetime

import jwt
import pytest

from weatherapp.jwtauth import (
    JWTAuthenticator,
    JWTDecodeError,
    JWTExpiredSignatureError,
    TokenPayload,
    TokenType,
    UserInfo,
)


@pytest.fixture
def auth():
    return JWTAuthenticator(secret_key="security_key")


def test_encode_decode_token(auth):
    now = datetime.now(UTC).replace(microsecond=0)
    now_t = int(now.timestamp())

    payload = TokenPayload(
        iat=now_t,
        exp=now_t + 60,
        token_type=TokenType.ACCESS,
        user_id=1,
    )
    token = auth.encode_token(payload)

    assert token > ""

    payload2 = auth.decode_token(token)

    assert payload2 == payload


def test_decode_token_expired(auth):
    now = datetime.now(UTC).replace(microsecond=0)
    now_t = int(now.timestamp())

    payload = TokenPayload(
        iat=now_t - 120,
        exp=now_t - 60,
        token_type=TokenType.ACCESS,
        user_id=1,
    )
    token = auth.encode_token(payload)

    with pytest.raises(JWTExpiredSignatureError):
        auth.decode_token(token)


def test_decode_token_invalid(auth):
    with pytest.raises(JWTDecodeError):
        auth.decode_token("invalid")


def test_create_token_for_user(auth):
    now = datetime.now(UTC).replace(microsecond=0)

    user = UserInfo(user_id=1)
    info = auth.create_token_for_user(user, now=now)

    assert info.token_access > ""
    assert info.token_refresh > ""

    assert info.token_access_expires_at == now + auth.access_token_life_time
    assert info.token_refresh_expires_at == now + auth.refresh_token_life_time

    payload = jwt.decode(
        info.token_access, auth.secret_key, algorithms=[auth.algorithm]
    )
    assert payload["user_id"] == 1

    payload = jwt.decode(
        info.token_refresh, auth.secret_key, algorithms=[auth.algorithm]
    )
    assert payload["user_id"] == 1
