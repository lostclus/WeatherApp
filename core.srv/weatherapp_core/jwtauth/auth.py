import logging
from typing import Any

from django.http import HttpRequest
from ninja.security import HttpBearer

from weatherapp_core.users.models import User

from .logic import decode_token
from .schema import TokenPayload, TokenType

log = logging.getLogger(__name__)


def get_token(request: HttpRequest) -> str | None:
    value = request.headers.get("Authorization")
    if not value:
        return None
    if value.startswith("Bearer "):
        value = value[len("Bearer ") :]
    return value


def get_token_payload(token: str) -> TokenPayload | None:
    if not token:
        log.debug("No authentication key")
        return None

    payload = decode_token(token)
    if not payload:
        log.debug("Key verification failed")
        return None

    if payload.token_type != TokenType.ACCESS:
        log.debug("Invalid token type")
        return None

    return payload


def auth_request(request: HttpRequest, token: str | None = None) -> User | None:
    if token is None:
        token = get_token(request)
    if token is None:
        return None

    payload = get_token_payload(token)
    if not payload:
        return None

    try:
        user = User.objects.filter(pk=payload.user_id).get()
    except User.DoesNotExist:
        log.debug("User doesn't exists")
        return None

    return user


async def async_auth_request(
    request: HttpRequest, token: str | None = None
) -> User | None:
    if token is None:
        token = get_token(request)
    if token is None:
        return None

    payload = get_token_payload(token)
    if not payload:
        return None

    try:
        user = await User.objects.filter(pk=payload.user_id).aget()
    except User.DoesNotExist:
        return None

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
