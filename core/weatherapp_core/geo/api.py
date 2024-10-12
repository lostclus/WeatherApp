from typing import Any, cast

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

from .models import Location


class LocationService(ModelService):
    def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
        route_context = cast(RouteContext, service_resolver(RouteContext))
        request = cast(HttpRequest, route_context.request)
        user = request.user
        assert user.is_authenticated
        return super().create(schema, user=user, **kwargs)


class IsOwned(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: Any) -> bool:
        return request.user.is_authenticated

    def has_object_permission(
        self, request: HttpRequest, controller: Any, obj: Location
    ) -> bool:
        return request.user == obj.user or (
            obj.user is None and request.method in permissions.SAFE_METHODS
        )


@api_controller("/locations", permissions=[IsOwned])
class LocationsController(ModelControllerBase):
    service = LocationService(Location)
    model_config = ModelConfig(
        model=Location,
        schema_config=ModelSchemaConfig(exclude={"user"}),
    )
