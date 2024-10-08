import zoneinfo
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

TimeZone = models.TextChoices(
    "TimeZone", " ".join(tz for tz in sorted(zoneinfo.available_timezones()))
)


class TemperatureUnit(models.TextChoices):
    CELSIUS = "celsius", _("Celsius °C")
    FAHRENHEIT = "fahrenheit", _("Fahrenheit °F")


class WindSpeedUnit(models.TextChoices):
    KM_H = "km/h", _("Km/h")
    M_S = "m/s", _("m/s")
    MPH = "mph", _("Mph")
    KNOTS = "knots", _("Knots")


class PrecipitationUnit(models.TextChoices):
    MILLIMETER = "millimeter", _("Millimeter")
    INCH = "inch", _("Inch")


class DateFormat(models.TextChoices):
    ISO_8601 = "YYYY-MM-DD", _("ISO 8601 (e.g. 2001-12-31)")
    DD_MM_YYYY = "DD/MM/YYYY", _("DD/MM/YYYY (e.g. 31/12/2001)")
    MM_DD_YYYY = "MM/DD/YYYY", _("MM/DD/YYYY (e.g. 12/31/2001)")
    DD_MM_YYYY_DS = "DD.MM.YYYY", _("DD.MM.YYYY (e.g. 31.12.2001)")


class TimeFormat(models.TextChoices):
    H24 = "HH:mm", _("24 hours")
    H12 = "hh:MM a", _("12 hours")


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
        choices=TimeZone,  # type: ignore
        default=settings.TIME_ZONE,
    )
    temperature_unit = models.CharField(
        verbose_name=_("temperature unit"),
        max_length=100,
        choices=TemperatureUnit,
        default=TemperatureUnit.CELSIUS,
    )
    wind_speed_unit = models.CharField(
        _("wind speed unit"),
        max_length=100,
        choices=WindSpeedUnit,
        default=WindSpeedUnit.M_S,
    )
    precipitation_unit = models.CharField(
        _("precipitation unit"),
        max_length=100,
        choices=PrecipitationUnit,
        default=PrecipitationUnit.MILLIMETER,
    )
    date_format = models.CharField(
        _("date format"),
        max_length=100,
        choices=DateFormat,
        default=DateFormat.ISO_8601,
    )
    time_format = models.CharField(
        _("time format"),
        max_length=100,
        choices=TimeFormat,
        default=TimeFormat.H24,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
