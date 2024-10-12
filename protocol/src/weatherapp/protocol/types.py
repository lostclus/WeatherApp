import zoneinfo
from enum import Enum

TimeZone = Enum(  # type: ignore
    "TimeZoneChoices",
    [tz for tz in sorted(zoneinfo.available_timezones())],
)


class TemperatureUnit(str, Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class WindSpeedUnit(str, Enum):
    KM_H = "km/h"
    M_S = "m/s"
    MPH = "mph"
    KNOTS = "knots"


class PrecipitationUnit(str, Enum):
    MILLIMETER = "millimeter"
    INCH = "inch"


class DateFormat(str, Enum):
    ISO_8601 = "YYYY-MM-DD"
    DD_MM_YYYY = "DD/MM/YYYY"
    MM_DD_YYYY = "MM/DD/YYYY"
    DD_MM_YYYY_DS = "DD.MM.YYYY"


class TimeFormat(str, Enum):
    H24 = "HH:mm"
    H12 = "hh:MM a"
