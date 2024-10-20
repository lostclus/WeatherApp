from http import HTTPStatus

from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from ninja import Router
from ninja.errors import HttpError, ValidationError

from weatherapp_core.geo.models import Location

from .models import User
from .schema import UserCreateSchema, UserOutSchema, UserUpdateSchema

users_router = Router(tags=["users"])


def _users() -> models.QuerySet[User]:
    return User.objects.annotate(
        default_location_id=models.F("default_location__location_id"),
    )


@users_router.post("/", response={HTTPStatus.CREATED: UserOutSchema}, auth=None)
async def create_user(request: HttpRequest, payload: UserCreateSchema) -> User:
    if await User.objects.filter(email=payload.email).aexists():
        raise ValidationError([{"msg": _("User already exists."), "loc": ["email"]}])

    user = User(email=payload.email)
    user.set_password(payload.password)
    await user.asave()

    # Give admin rights to the first registered user
    if user.pk == 1:
        user.is_superuser = True
        user.is_staff = True
        await user.asave()

    user.default_location_id = None  # type: ignore

    return user


@users_router.get("/{int:user_id}", response=UserOutSchema)
async def get_user(request: HttpRequest, user_id: int) -> User:
    if user_id != request.user.pk:
        raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")

    user = await _users().aget(pk=user_id)
    return user


@users_router.patch("/{int:user_id}", response=UserOutSchema)
async def update_user(
    request: HttpRequest, user_id: int, payload: UserUpdateSchema
) -> User:
    if user_id != request.user.pk:
        raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")

    user = await _users().aget(pk=user_id)
    kw = payload.dict()
    default_location_id = kw.pop("default_location_id", None)

    for attr, value in kw.items():
        setattr(user, attr, value)
    await user.asave()

    if default_location_id:
        loc = await Location.objects.aget(pk=default_location_id)
        await loc.aset_default_for(user)
        user = await _users().aget(pk=user_id)

    return user
