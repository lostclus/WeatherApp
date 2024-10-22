import logging
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from weatherapp.jwtauth import (
    JWTAuthenticator,
    JWTTokenRequired,
    JWTUserNotExist,
    TokenPayload,
    TokenType,
)

from weatherapp_core.users.models import User

log = logging.getLogger(__name__)


def get_authenticator() -> JWTAuthenticator:
    return JWTAuthenticator(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_life_time=settings.JWT_ACCESS_TOKEN_LIFETIME,
        refresh_token_life_time=settings.JWT_REFRESH_TOKEN_LIFETIME,
    )


def get_token(request: HttpRequest) -> str | None:
    value = request.headers.get("Authorization")
    if not value:
        return None
    if value.startswith("Bearer "):
        value = value[len("Bearer ") :]
    return value


def get_token_payload(token: str) -> TokenPayload:
    authenticator = get_authenticator()
    payload = authenticator.decode_token(token, assert_type=TokenType.ACCESS)
    return payload


def auth_request(request: HttpRequest, token: str | None = None) -> User | None:
    if token is None:
        token = get_token(request)
    if token is None:
        raise JWTTokenRequired("No authentication token provided")

    payload = get_token_payload(token)
    try:
        user = User.objects.filter(pk=payload.user_id).get()
    except User.DoesNotExist as error:
        raise JWTUserNotExist("User doesn't exists") from error

    request.user = user
    return user


async def async_auth_request(
    request: HttpRequest, token: str | None = None
) -> User | None:
    if token is None:
        token = get_token(request)
    if token is None:
        raise JWTTokenRequired("No authentication token provided")

    payload = get_token_payload(token)
    try:
        user = await User.objects.filter(pk=payload.user_id).aget()
    except User.DoesNotExist as error:
        raise JWTUserNotExist("User doesn't exists") from error

    request.user = user
    return user


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any:
        return auth_request(request, token=token)


class AsyncJWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any:
        return token

    async def __call__(self, request: HttpRequest) -> Any:
        token = super().__call__(request)
        return await async_auth_request(request, token=token)
