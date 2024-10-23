import zoneinfo
from django.db import models
from django.utils.translation import gettext_lazy as _
from weatherapp.protocol import (
    AggregateFunction,
    AggregateGroup,
    DateFormat,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit,
)

TimeZoneChoices = models.TextChoices(
    "TimeZoneChoices",
    ((tz, tz) for tz in sorted(zoneinfo.available_timezones())),  # type: ignore
)


class TemperatureUnitChoices(models.TextChoices):
    CELSIUS = TemperatureUnit.CELSIUS, _("Celsius °C")
    FAHRENHEIT = TemperatureUnit.FAHRENHEIT, _("Fahrenheit °F")


class WindSpeedUnitChoices(models.TextChoices):
    KM_H = WindSpeedUnit.KM_H, _("Km/h")
    M_S = WindSpeedUnit.M_S, _("m/s")
    MPH = WindSpeedUnit.MPH, _("Mph")
    KNOTS = WindSpeedUnit.KNOTS, _("Knots")


class PrecipitationUnitChoices(models.TextChoices):
    MILLIMETER = PrecipitationUnit.MILLIMETER, _("Millimeter")
    INCH = PrecipitationUnit.INCH, _("Inch")


class DateFormatChoices(models.TextChoices):
    ISO_8601 = DateFormat.ISO_8601, _("ISO 8601 (e.g. 2001-12-31)")
    DD_MM_YYYY = DateFormat.DD_MM_YYYY, _("DD/MM/YYYY (e.g. 31/12/2001)")
    MM_DD_YYYY = DateFormat.MM_DD_YYYY, _("MM/DD/YYYY (e.g. 12/31/2001)")
    DD_MM_YYYY_DS = DateFormat.DD_MM_YYYY_DS, _("DD.MM.YYYY (e.g. 31.12.2001)")


class TimeFormatChoices(models.TextChoices):
    H24 = TimeFormat.H24, _("24 hours")
    H12 = TimeFormat.H12, _("12 hours")


class AggregateGroupChoices(models.TextChoices):
    DAY = AggregateGroup.DAY, _("Day")
    WEEK = AggregateGroup.WEEK, _("Week")
    MONTH = AggregateGroup.MONTH, _("Month")
    YEAR = AggregateGroup.YEAR, _("Year")


class AggregateFunctionChoices(models.TextChoices):
    MIN = AggregateFunction.MIN, _("Min")
    MAX = AggregateFunction.MAX, _("Max")
    AVG = AggregateFunction.AVG, _("Avg")
    MEDIAN = AggregateFunction.MEDIAN, _("Median")
    DIFF_MAX_MIN = AggregateFunction.DIFF_MAX_MIN, _("Max-Min")
