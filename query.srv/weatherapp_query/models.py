from weatherapp.protocol import Weather as WeatherProto
from weatherapp.protocol import WeatherData, WeatherDataField

from .types import DateTimeConvertTZ

__all__ = ["Weather", "WeatherData", "WeatherDataField"]


class Weather(WeatherProto):
    timestamp: DateTimeConvertTZ
