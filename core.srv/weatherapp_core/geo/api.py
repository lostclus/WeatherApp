from http import HTTPStatus

from django.db import models
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router

from weatherapp_core.users.models import User

from .models import DefaultLocation, Location
from .schema import LocationInSchema, LocationOutSchema

locations_router = Router(tags=["locations"])


def _user_locations(user: User, only_my: bool = False) -> models.QuerySet[Location]:
    queryset = Location.objects.all()
    queryset_my = queryset.filter(user=user)
    queryset_sys = queryset.filter(user=None)

    if only_my:
        queryset = queryset_my
    else:
        queryset = queryset_my | queryset_sys

    return queryset.annotate(
        is_default=models.Exists(
            DefaultLocation.objects.filter(user=user, location=models.OuterRef("pk"))
        )
    )


@locations_router.post("/", response={HTTPStatus.CREATED: LocationOutSchema})
async def create_location(request: HttpRequest, payload: LocationInSchema) -> Location:
    user = request.user
    assert isinstance(user, User)

    kw = payload.dict()
    is_default = kw.pop("is_default")
    loc = await Location.objects.acreate(user=user, **kw)
    if is_default:
        await loc.aset_default_for(user)
    loc.is_default = is_default  # type: ignore

    return loc


@locations_router.get("/", response=list[LocationOutSchema])
async def list_locations(request: HttpRequest) -> list[Location]:
    user = request.user
    assert isinstance(user, User)
    queryset = _user_locations(user).select_related("user").order_by("name")
    return [obj async for obj in queryset]


@locations_router.get("/my", response=list[LocationOutSchema])
async def list_my_locations(request: HttpRequest) -> list[Location]:
    user = request.user
    assert isinstance(user, User)

    queryset = (
        _user_locations(user, only_my=True).select_related("user").order_by("name")
    )
    return [obj async for obj in queryset]


@locations_router.get("/{int:location_id}", response=LocationOutSchema)
async def get_location(request: HttpRequest, location_id: int) -> Location:
    user = request.user
    assert isinstance(user, User)

    queryset = _user_locations(user)
    loc = await aget_object_or_404(queryset, pk=location_id)
    return loc


@locations_router.put("/{int:location_id}", response=LocationOutSchema)
async def update_location(
    request: HttpRequest, location_id: int, payload: LocationInSchema
) -> Location:
    user = request.user
    assert isinstance(user, User)

    queryset = _user_locations(user)
    loc = await aget_object_or_404(queryset, pk=location_id)

    kw = payload.dict()
    is_default = kw.pop("is_default")

    for attr, value in kw.items():
        setattr(loc, attr, value)

    await loc.asave()

    if is_default:
        await loc.aset_default_for(user)

    return loc


@locations_router.delete("/{int:location_id}", response={HTTPStatus.NO_CONTENT: None})
async def delete_location(request: HttpRequest, location_id: int) -> None:
    user = request.user
    assert isinstance(user, User)

    queryset = _user_locations(user)
    loc = await aget_object_or_404(queryset, pk=location_id)
    await loc.adelete()
