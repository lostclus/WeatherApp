import itertools

from pydantic import create_model
from weatherapp.protocol import AggregateFunction, WeatherDataField
from weatherapp.protocol import Weather as WeatherProto
from weatherapp.protocol import WeatherData as WeatherDataProto

from .types import DateTime, Precipitation, Temperature, WindSpeed


class WeatherData(WeatherDataProto):
    temperature_2m: Temperature | None = None
    apparent_temperature: Temperature | None = None
    precipitation: Precipitation | None = None
    wind_speed_10m: WindSpeed | None = None
    wind_speed_100m: WindSpeed | None = None


class Weather(WeatherData, WeatherProto):
    timestamp: DateTime


_weather_data_fields = WeatherData.model_fields
_weather_fields = Weather.model_fields
_meta_fields = {
    field: (info.annotation, info)
    for field, info in _weather_fields.items()
    if field in ("timestamp", "location_id")
}

WeatherAggregated = create_model(  # type: ignore
    "WeatherAggregated",
    **{
        **_meta_fields,
        **{
            f"{field}_{func}": (
                _weather_data_fields[field].annotation,
                _weather_data_fields[field],
            )
            for field, func in itertools.product(WeatherDataField, AggregateFunction)
        },
    },
)
