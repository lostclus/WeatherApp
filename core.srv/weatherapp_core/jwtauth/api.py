from http import HTTPStatus

from django.contrib.auth import aauthenticate
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from weatherapp_core.users.models import User

from .logic import create_token_for_user, decode_token
from .schema import TokenCreateSchema, TokenOutSchema, TokenRefreshSchema, TokenType

auth_router = Router(tags=["auth"])


@auth_router.post("/", response=TokenOutSchema, auth=None)
async def create_token(
    request: HttpRequest, payload: TokenCreateSchema
) -> TokenOutSchema:
    user = await aauthenticate(email=payload.email, password=payload.password)
    if user is None:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "Authentication failed")
    token = create_token_for_user(user)
    return token


@auth_router.post("/refresh", response=TokenOutSchema, auth=None)
async def refresh_token(
    request: HttpRequest, payload: TokenRefreshSchema
) -> TokenOutSchema:
    token_payload = decode_token(payload.token_refresh)
    if not token_payload:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "Authentication failed")

    if token_payload.token_type != TokenType.REFRESH:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token type")

    try:
        user = await User.objects.aget(pk=token_payload.user_id)
    except User.DoesNotExist as error:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "User not found") from error

    token = create_token_for_user(user)
    return token
