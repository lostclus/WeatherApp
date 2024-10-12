from decimal import Decimal

import pytest
from pydantic import ValidationError

from weatherapp.protocol.bus import Location, User
from weatherapp.protocol.types import (
    DateFormat,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    TimeZone,
    WindSpeedUnit,
)


def test_location_null_island():
    location = Location(
        id=1,
        name="Null island",
        latitude=Decimal(0),
        longitude=Decimal(0),
        user_id=None,
        is_default=False,
        is_active=True,
    )
    assert location


def test_location_invalid_latitude():
    with pytest.raises(ValidationError):
        Location(
            id=1,
            name="Invalid",
            latitude=Decimal(91),
            longitude=Decimal(0),
            user_id=None,
            is_default=False,
            is_active=True,
        )


def test_location_invalid_longitude():
    with pytest.raises(ValidationError):
        Location(
            id=1,
            name="Invalid",
            latitude=Decimal(0),
            longitude=Decimal(181),
            user_id=None,
            is_default=False,
            is_active=True,
        )


def test_user():
    user = User(
        id=1,
        email="test@example.com",
        timezone=TimeZone.UTC,
        temperature_unit=TemperatureUnit.CELSIUS,
        wind_speed_unit=WindSpeedUnit.M_S,
        precipitation_unit=PrecipitationUnit.MILLIMETER,
        date_format=DateFormat.ISO_8601,
        time_format=TimeFormat.H24,
        is_active=True,
    )
    assert user


def test_user_invalid_email():
    with pytest.raises(ValidationError):
        User(
            id=1,
            email="invalid",
            timezone=TimeZone.UTC,
            temperature_unit=TemperatureUnit.CELSIUS,
            wind_speed_unit=WindSpeedUnit.M_S,
            precipitation_unit=PrecipitationUnit.MILLIMETER,
            date_format=DateFormat.ISO_8601,
            time_format=TimeFormat.H24,
            is_active=True,
        )


def test_user_invalid_timezone():
    with pytest.raises(ValidationError):
        User(
            id=1,
            email="test@example.com",
            timezone="invalid",
            temperature_unit=TemperatureUnit.CELSIUS,
            wind_speed_unit=WindSpeedUnit.M_S,
            precipitation_unit=PrecipitationUnit.MILLIMETER,
            date_format=DateFormat.ISO_8601,
            time_format=TimeFormat.H24,
            is_active=True,
        )
