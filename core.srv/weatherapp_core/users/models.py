from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from weatherapp_core.constants import (
    DateFormatChoices,
    PrecipitationUnitChoices,
    TemperatureUnitChoices,
    TimeFormatChoices,
    TimeZoneChoices,
    WindSpeedUnitChoices,
)


class User(AbstractUser):
    # Remove username field
    username = None  # type: ignore

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
    )
    timezone = models.CharField(
        verbose_name=_("time zone"),
        max_length=100,
        choices=TimeZoneChoices,
        default=settings.TIME_ZONE,
    )
    temperature_unit = models.CharField(
        verbose_name=_("temperature unit"),
        max_length=100,
        choices=TemperatureUnitChoices,
        default=TemperatureUnitChoices.CELSIUS,
    )
    wind_speed_unit = models.CharField(
        _("wind speed unit"),
        max_length=100,
        choices=WindSpeedUnitChoices,
        default=WindSpeedUnitChoices.M_S,
    )
    precipitation_unit = models.CharField(
        _("precipitation unit"),
        max_length=100,
        choices=PrecipitationUnitChoices,
        default=PrecipitationUnitChoices.MILLIMETER,
    )
    date_format = models.CharField(
        _("date format"),
        max_length=100,
        choices=DateFormatChoices,
        default=DateFormatChoices.ISO_8601,
    )
    time_format = models.CharField(
        _("time format"),
        max_length=100,
        choices=TimeFormatChoices,
        default=TimeFormatChoices.H24,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
