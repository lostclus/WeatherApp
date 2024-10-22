from http import HTTPStatus

from django.contrib.auth import aauthenticate
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from weatherapp.jwtauth import JWTUserNotExist, TokenType, UserInfo

from weatherapp_core.users.models import User

from .auth import get_authenticator
from .schema import TokenCreateSchema, TokenOutSchema, TokenRefreshSchema

auth_router = Router(tags=["auth"])


@auth_router.post("/", response=TokenOutSchema, auth=None)
async def create_token(
    request: HttpRequest, payload: TokenCreateSchema
) -> TokenOutSchema:
    user = await aauthenticate(email=payload.email, password=payload.password)
    if user is None:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "Authentication failed")

    authenticator = get_authenticator()
    info = authenticator.create_token_for_user(UserInfo(user_id=user.pk))
    token = TokenOutSchema(
        user_id=user.pk,
        email=user.email,
        **info.model_dump(),
    )
    return token


@auth_router.post("/refresh", response=TokenOutSchema, auth=None)
async def refresh_token(
    request: HttpRequest, payload: TokenRefreshSchema
) -> TokenOutSchema:

    authenticator = get_authenticator()
    token_payload = authenticator.decode_token(
        payload.token_refresh, assert_type=TokenType.REFRESH
    )

    try:
        user = await User.objects.aget(pk=token_payload.user_id)
    except User.DoesNotExist as error:
        raise JWTUserNotExist("User not found") from error

    info = authenticator.create_token_for_user(UserInfo(user_id=user.pk))
    token = TokenOutSchema(
        user_id=user.pk,
        email=user.email,
        **info.model_dump(),
    )
    return token
