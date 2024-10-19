from weatherapp.protocol import Weather as WeatherProto
from weatherapp.protocol import WeatherData, WeatherDataField

from .types import DateTime, Precipitation, Temperature, WindSpeed

__all__ = ["Weather", "WeatherData", "WeatherDataField"]


class Weather(WeatherProto):
    timestamp: DateTime
    temperature_2m: Temperature | None = None
    apparent_temperature: Temperature | None = None
    precipitation: Precipitation | None = None
    wind_speed_10m: WindSpeed | None = None
    wind_speed_100m: WindSpeed | None = None
