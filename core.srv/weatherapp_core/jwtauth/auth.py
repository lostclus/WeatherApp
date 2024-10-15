import logging

from django.http import HttpRequest

from weatherapp_core.users.models import User

from .logic import decode_token
from .schema import TokenPayload, TokenType

log = logging.getLogger(__name__)


def get_key(request: HttpRequest) -> str | None:
    value = request.headers.get("Authorization")
    if not value:
        return None
    if value.startswith("Bearer "):
        value = value[len("Bearer ") :]
    return value


def get_token_payload(request: HttpRequest) -> TokenPayload | None:
    key = get_key(request)
    if not key:
        log.debug("No authentication key")
        return None

    payload = decode_token(key)
    if not payload:
        log.debug("Key verification failed")
        return None

    if payload.token_type != TokenType.ACCESS:
        log.debug("Invalid token type")
        return None

    return payload


def auth_request(request: HttpRequest) -> User | None:
    payload = get_token_payload(request)
    if not payload:
        return None

    try:
        user = User.objects.filter(pk=payload.user_id).get()
    except User.DoesNotExist:
        log.debug("User doesn't exists")
        return None

    return user


async def async_auth_request(request: HttpRequest) -> User | None:
    payload = get_token_payload(request)
    if not payload:
        return None

    try:
        user = await User.objects.filter(pk=payload.user_id).aget()
    except User.DoesNotExist:
        return None

    request.user = user
    return user
