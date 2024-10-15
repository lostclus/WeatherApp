from http import HTTPStatus

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from ninja import Router
from ninja.errors import HttpError, ValidationError

from .models import User
from .schema import UserCreateSchema, UserOutSchema, UserUpdateSchema

users_router = Router()


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

    return user


@users_router.get("/{int:user_id}", response=UserOutSchema)
async def get_user(request: HttpRequest, user_id: int) -> User:
    if user_id != request.user.pk:
        raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")

    user = await User.objects.aget(pk=user_id)
    return user


@users_router.patch("/{int:user_id}", response=UserOutSchema)
async def update_user(
    request: HttpRequest, user_id: int, payload: UserUpdateSchema
) -> User:
    if user_id != request.user.pk:
        raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")

    user = await User.objects.aget(pk=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    await user.asave()
    return user
