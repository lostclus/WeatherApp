from http import HTTPStatus

from django.db import models
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router

from weatherapp_core.users.models import User

from .models import Location
from .schema import LocationInSchema, LocationOutSchema

locations_router = Router(tags=["locations"])


def _user_locations(request: HttpRequest) -> models.QuerySet[Location]:
    user = request.user
    assert isinstance(user, User)
    queryset = Location.objects.all()
    queryset_my = queryset.filter(user=user)
    queryset_sys = queryset.filter(user=None)
    queryset = queryset_my | queryset_sys
    return queryset


@locations_router.post("/", response={HTTPStatus.CREATED: LocationOutSchema})
async def create_location(request: HttpRequest, payload: LocationInSchema) -> Location:
    user = request.user
    assert isinstance(user, User)

    if payload.is_default:  # type: ignore
        queryset = _user_locations(request)
        await queryset.filter(user=user).aupdate(is_default=False)

    loc = await Location.objects.acreate(user=user, **payload.dict())
    return loc


@locations_router.get("/", response=list[LocationOutSchema])
async def list_locations(request: HttpRequest) -> list[Location]:
    queryset = _user_locations(request).select_related("user")
    return [obj async for obj in queryset]


@locations_router.get("/my", response=list[LocationOutSchema])
async def list_my_locations(request: HttpRequest) -> list[Location]:
    user = request.user
    assert isinstance(user, User)
    queryset = _user_locations(request).filter(user=user)
    return [obj async for obj in queryset]


@locations_router.get("/{int:location_id}", response=LocationOutSchema)
async def get_location(request: HttpRequest, location_id: int) -> Location:
    queryset = _user_locations(request)
    loc = await aget_object_or_404(queryset, pk=location_id)
    return loc


@locations_router.put("/{int:location_id}", response=LocationOutSchema)
async def update_location(
    request: HttpRequest, location_id: int, payload: LocationInSchema
) -> Location:
    queryset = _user_locations(request)
    loc = await aget_object_or_404(queryset, pk=location_id)

    if payload.is_default:  # type: ignore
        user = request.user
        assert isinstance(user, User)
        await queryset.filter(user=user).exclude(pk=loc.pk).aupdate(is_default=False)

    for attr, value in payload.dict().items():
        setattr(loc, attr, value)
    await loc.asave()

    return loc


@locations_router.delete("/{int:location_id}", response={HTTPStatus.NO_CONTENT: None})
async def delete_location(request: HttpRequest, location_id: int) -> None:
    queryset = _user_locations(request)
    loc = await aget_object_or_404(queryset, pk=location_id)
    await loc.adelete()
