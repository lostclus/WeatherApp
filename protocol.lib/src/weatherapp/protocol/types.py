import zoneinfo
from enum import StrEnum

TimeZone = StrEnum(  # type: ignore
    "TimeZone",
    [(tz, tz) for tz in sorted(zoneinfo.available_timezones())],
)


class TemperatureUnit(StrEnum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class WindSpeedUnit(StrEnum):
    KM_H = "km/h"
    M_S = "m/s"
    MPH = "mph"
    KNOTS = "knots"


class PrecipitationUnit(StrEnum):
    MILLIMETER = "millimeter"
    INCH = "inch"


class DateFormat(StrEnum):
    ISO_8601 = "YYYY-MM-DD"
    DD_MM_YYYY = "DD/MM/YYYY"
    MM_DD_YYYY = "MM/DD/YYYY"
    DD_MM_YYYY_DS = "DD.MM.YYYY"


class TimeFormat(StrEnum):
    H24 = "HH:mm"
    H12 = "hh:MM a"


class AggregateFunction(StrEnum):
    MIN = "min"
    MAX = "max"
    AVG = "avg"
    MEDIAN = "median"
    DIFF_MAX_MIN = "diff_max_min"


class AggregateGroup(StrEnum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
