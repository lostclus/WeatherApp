import zoneinfo
from django.db import models
from django.utils.translation import gettext_lazy as _

TimeZoneChoices = models.TextChoices(
    "TimeZoneChoices",
    ((tz, tz) for tz in sorted(zoneinfo.available_timezones())),  # type: ignore
)


class TemperatureUnitChoices(models.TextChoices):
    CELSIUS = "celsius", _("Celsius °C")
    FAHRENHEIT = "fahrenheit", _("Fahrenheit °F")


class WindSpeedUnitChoices(models.TextChoices):
    KM_H = "km/h", _("Km/h")
    M_S = "m/s", _("m/s")
    MPH = "mph", _("Mph")
    KNOTS = "knots", _("Knots")


class PrecipitationUnitChoices(models.TextChoices):
    MILLIMETER = "millimeter", _("Millimeter")
    INCH = "inch", _("Inch")


class DateFormatChoices(models.TextChoices):
    ISO_8601 = "YYYY-MM-DD", _("ISO 8601 (e.g. 2001-12-31)")
    DD_MM_YYYY = "DD/MM/YYYY", _("DD/MM/YYYY (e.g. 31/12/2001)")
    MM_DD_YYYY = "MM/DD/YYYY", _("MM/DD/YYYY (e.g. 12/31/2001)")
    DD_MM_YYYY_DS = "DD.MM.YYYY", _("DD.MM.YYYY (e.g. 31.12.2001)")


class TimeFormatChoices(models.TextChoices):
    H24 = "HH:mm", _("24 hours")
    H12 = "hh:MM a", _("12 hours")
