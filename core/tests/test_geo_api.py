from decimal import Decimal

import pytest

from weatherapp_core.geo.models import Location
from weatherapp_core.users.models import User


@pytest.fixture
def location(user):
    location = Location.objects.create(
        name="Null island",
        latitude=Decimal(0),
        longitude=Decimal(0),
        user=user,
    )
    return location


@pytest.fixture
def other_user():
    other_user = User.objects.create(email="other@example.com")
    return other_user


@pytest.mark.django_db(transaction=True)
def test_location_create(client, user, auth_headers):
    response = client.post(
        "/core/api/v1/locations/",
        data={
            "name": "Test location",
            "latitude": "1.23",
            "longitude": "4.56",
        },
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 201, response.content
    response_data = response.json()

    location_id = response_data["id"]

    assert response_data == {
        "id": location_id,
        "name": "Test location",
        "latitude": "1.23",
        "longitude": "4.56",
        "is_default": False,
        "is_active": True,
    }

    location = Location.objects.get(pk=location_id)
    assert location.name == "Test location"
    assert location.latitude == Decimal("1.23")
    assert location.longitude == Decimal("4.56")
    assert location.is_default is False
    assert location.is_active is True
    assert location.user == user


@pytest.mark.django_db(transaction=True)
def test_location_get(client, user, auth_headers, location):
    response = client.get(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "id": location.pk,
        "name": "Null island",
        "latitude": "0.00000",
        "longitude": "0.00000",
        "is_default": False,
        "is_active": True,
    }


@pytest.mark.django_db(transaction=True)
def test_location_get_system(client, user, auth_headers, location):
    location.user = None
    location.save()

    response = client.get(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "id": location.pk,
        "name": "Null island",
        "latitude": "0.00000",
        "longitude": "0.00000",
        "is_default": False,
        "is_active": True,
    }


@pytest.mark.django_db(transaction=True)
def test_location_get_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.get(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )

    assert response.status_code == 403, response.content


@pytest.mark.django_db(transaction=True)
def test_location_update(client, user, auth_headers, location):
    response = client.patch(
        f"/core/api/v1/locations/{location.pk}",
        data={
            "name": "Name updated",
        },
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == {
        "id": location.pk,
        "name": "Name updated",
        "latitude": "0.00000",
        "longitude": "0.00000",
        "is_default": False,
        "is_active": True,
    }

    location.refresh_from_db()
    assert location.name == "Name updated"


@pytest.mark.django_db(transaction=True)
def test_location_update_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.patch(
        f"/core/api/v1/locations/{location.pk}",
        data={
            "name": "Name updated",
        },
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == 403, response.content


@pytest.mark.django_db(transaction=True)
def test_location_delete(client, user, auth_headers, location):
    location_id = location.pk

    response = client.delete(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )
    assert response.status_code == 204, response.content

    assert not Location.objects.filter(pk=location_id).exists()


@pytest.mark.django_db(transaction=True)
def test_location_delete_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.delete(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )
    assert response.status_code == 403, response.content
