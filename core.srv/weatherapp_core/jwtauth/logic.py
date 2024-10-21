from datetime import UTC, datetime

import jwt
from django.conf import settings

from weatherapp_core.users.models import User

from .schema import TokenOutSchema, TokenPayload, TokenType


def encode_token(payload: TokenPayload) -> str:
    return jwt.encode(
        payload.dict(), settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> TokenPayload | None:
    try:
        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.DecodeError:
        return None
    payload = TokenPayload(**decoded)
    return payload


def create_token_for_user(user: User, now: datetime | None = None) -> TokenOutSchema:
    now = (now or datetime.now(UTC)).replace(microsecond=0)
    exp_access = now + settings.JWT_ACCESS_TOKEN_LIFETIME
    exp_refresh = now + settings.JWT_REFRESH_TOKEN_LIFETIME

    access_payload = TokenPayload(
        exp=int(exp_access.timestamp()),
        iat=int(now.timestamp()),
        token_type=TokenType.ACCESS,
        user_id=user.pk,
    )
    refresh_payload = TokenPayload(
        exp=int(exp_refresh.timestamp()),
        iat=int(now.timestamp()),
        token_type=TokenType.REFRESH,
        user_id=user.pk,
    )

    token_access = encode_token(access_payload)
    token_refresh = encode_token(refresh_payload)

    return TokenOutSchema(
        email=user.email,
        user_id=user.pk,
        token_access=token_access,
        token_refresh=token_refresh,
        token_access_expires_at=exp_access,
    )
