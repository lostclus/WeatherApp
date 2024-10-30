from decimal import Decimal

import pytest

from weatherapp_core.geo.models import Location

pytestmark = pytest.mark.django_db(transaction=True)


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
        "user": user.pk,
    }

    location = Location.objects.get(pk=location_id)
    assert location.name == "Test location"
    assert location.latitude == Decimal("1.23")
    assert location.longitude == Decimal("4.56")
    assert location.is_active is True
    assert location.user == user


def test_location_create_is_default(client, user, auth_headers):
    response = client.post(
        "/core/api/v1/locations/",
        data={
            "name": "Test location",
            "latitude": "1.23",
            "longitude": "4.56",
            "is_default": True,
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
        "is_default": True,
        "is_active": True,
        "user": user.pk,
    }

    location = Location.objects.get(pk=location_id)
    assert location.name == "Test location"
    assert location.latitude == Decimal("1.23")
    assert location.longitude == Decimal("4.56")
    assert location.is_active is True
    assert location.user == user
    assert location.default_for.filter(user=user).exists()


def test_location_create_invalid_latitude(client, user, auth_headers):
    response = client.post(
        "/core/api/v1/locations/",
        data={
            "name": "Test location",
            "latitude": "91",
            "longitude": "4.56",
        },
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 422, response.content


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
        "user": user.pk,
    }


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
        "user": None,
    }


def test_location_get_is_default(client, user, auth_headers, location):
    location.default_for.create(user=user)

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
        "is_default": True,
        "is_active": True,
        "user": user.pk,
    }


def test_location_get_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.get(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )

    assert response.status_code == 404, response.content


def test_location_list(client, user, auth_headers, location, system_location):
    response = client.get("/core/api/v1/locations/", headers=auth_headers)

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == [
        {
            "id": location.pk,
            "name": "Null island",
            "latitude": "0.00000",
            "longitude": "0.00000",
            "is_default": False,
            "is_active": True,
            "user": user.pk,
        },
        {
            "id": system_location.pk,
            "name": "Some place",
            "latitude": "1.23000",
            "longitude": "4.56000",
            "is_default": False,
            "is_active": True,
            "user": None,
        },
    ]


def test_location_list_is_active(client, user, auth_headers, location, system_location):
    location.is_active = False
    location.save()
    system_location.is_active = True
    system_location.save()

    response = client.get(
        "/core/api/v1/locations/",
        {"is_active": True},
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert [data["id"] for data in response_data] == [system_location.pk]

    response = client.get(
        "/core/api/v1/locations/",
        {"is_active": False},
        headers=auth_headers,
    )

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert [data["id"] for data in response_data] == [location.pk]


def test_location_my_list(client, user, auth_headers, location):
    response = client.get("/core/api/v1/locations/my", headers=auth_headers)

    assert response.status_code == 200, response.content
    response_data = response.json()

    assert response_data == [
        {
            "id": location.pk,
            "name": "Null island",
            "latitude": "0.00000",
            "longitude": "0.00000",
            "is_default": False,
            "is_active": True,
            "user": user.pk,
        },
    ]


def test_location_update(client, user, auth_headers, location):
    response = client.put(
        f"/core/api/v1/locations/{location.pk}",
        data={
            "name": "Name updated",
            "latitude": "0.00000",
            "longitude": "0.00000",
            "is_default": False,
            "is_active": True,
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
        "user": user.pk,
    }

    location.refresh_from_db()
    assert location.name == "Name updated"


def test_location_update_invalid_latitude(client, user, auth_headers, location):
    response = client.put(
        f"/core/api/v1/locations/{location.pk}",
        data={
            "name": "Name updated",
            "latitude": "91",
            "longitude": "0.00000",
            "is_default": False,
            "is_active": True,
        },
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == 422, response.content


def test_location_update_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.put(
        f"/core/api/v1/locations/{location.pk}",
        data={
            "name": "Name updated",
            "latitude": "0.00000",
            "longitude": "0.00000",
            "is_default": False,
            "is_active": True,
        },
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == 404, response.content


def test_location_delete(client, user, auth_headers, location):
    location_id = location.pk

    response = client.delete(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )
    assert response.status_code == 204, response.content

    assert not Location.objects.filter(pk=location_id).exists()


def test_location_delete_unauthorized(client, user, auth_headers, location, other_user):
    location.user = other_user
    location.save()

    response = client.delete(
        f"/core/api/v1/locations/{location.pk}",
        headers=auth_headers,
    )
    assert response.status_code == 404, response.content
