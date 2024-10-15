from ninja import Schema


class ConstantsSchema(Schema):
    timezones: dict[str, str]
    temperature_units: dict[str, str]
    wind_speed_units: dict[str, str]
    precipitation_units: dict[str, str]
    date_formats: dict[str, str]
    time_formats: dict[str, str]
