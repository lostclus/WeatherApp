from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.http import HttpRequest
from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    ModelService,
    api_controller,
    permissions,
    service_resolver,
)
from ninja_extra.controllers import RouteContext
from pydantic import BaseModel as PydanticModel

from weatherapp_core.permissions import ReadOnly
from weatherapp_core.users.models import User

from .models import Location


class LocationService(ModelService):
    def _get_request_user(self) -> User | AnonymousUser:
        context = service_resolver(RouteContext)
        assert isinstance(context, RouteContext)
        request = context.request
        assert isinstance(request, HttpRequest)
        user = request.user
        return user

    async def create_async(self, schema: PydanticModel, **kwargs: Any) -> Any:
        user = self._get_request_user()
        assert user.is_authenticated
        return await super().create_async(schema, user=user, **kwargs)

    async def get_all_async(self, **kwargs: Any) -> models.QuerySet | list[Any]:
        user = self._get_request_user()
        assert user.is_authenticated
        queryset = await super().get_all_async()
        assert isinstance(queryset, models.QuerySet)
        queryset = queryset.filter(models.Q(user=user) | models.Q(user=None))
        return queryset


class IsLocationOwner(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: Any) -> bool:
        return True

    def has_object_permission(
        self, request: HttpRequest, controller: Any, obj: Location
    ) -> bool:
        return request.user.is_authenticated and request.user.pk == obj.user_id


class IsSystemLocation(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: Any) -> bool:
        return True

    def has_object_permission(
        self, request: HttpRequest, controller: Any, obj: Location
    ) -> bool:
        return obj.user_id is None


@api_controller(
    "/locations",
    permissions=[
        permissions.IsAuthenticated,
        IsLocationOwner | (ReadOnly & IsSystemLocation),  # type: ignore
    ],
)
class LocationsController(ModelControllerBase):
    service = LocationService(Location)
    model_config = ModelConfig(
        model=Location,
        async_routes=True,
        schema_config=ModelSchemaConfig(exclude=set(), read_only_fields=["user"]),
    )
