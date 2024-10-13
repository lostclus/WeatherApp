from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError, ValidationError
from ninja_extra import (
    ControllerBase,
    api_controller,
    http_generic,
    http_get,
    http_post,
    status,
)

from .models import User
from .schema import UserCreateSchema, UserEditSchema, UserOutSchema


@api_controller("/users")
class UsersController(ControllerBase):
    def _get_request_user(self) -> User | AnonymousUser:
        assert self.context
        request = self.context.request
        assert isinstance(request, HttpRequest)
        return request.user

    @transaction.atomic
    @http_post("/", auth=None, response={status.HTTP_201_CREATED: UserOutSchema})
    def create_user(self, payload: UserCreateSchema) -> User:
        if User.objects.filter(email=payload.email).exists():
            raise ValidationError(
                [{"msg": _("User already exists."), "loc": ["email"]}]
            )

        user = User(email=payload.email)
        user.set_password(payload.password)
        user.save()

        # Give admin rights to the first registered user
        if user.pk == 1:
            user.is_superuser = True
            user.is_staff = True
            user.save()

        return user

    @http_generic("/{int:user_id}", methods=["put", "patch"], response=UserOutSchema)
    async def update_user(self, user_id: int, payload: UserEditSchema) -> User:
        request_user = self._get_request_user()
        if user_id != request_user.pk:
            raise HttpError(status.HTTP_403_FORBIDDEN, "Permission denied")

        user = await User.objects.aget(pk=user_id)
        for attr, value in payload.dict().items():
            setattr(user, attr, value)
        await user.asave()
        return user

    @http_get("/{int:user_id}", response=UserOutSchema)
    async def get_user_by_id(self, user_id: int) -> User:
        request_user = self._get_request_user()
        if user_id != request_user.pk:
            raise HttpError(status.HTTP_403_FORBIDDEN, "Permission denied")

        user = await User.objects.aget(pk=user_id)
        return user
