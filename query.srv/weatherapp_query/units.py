from weatherapp.protocol import PrecipitationUnit, TemperatureUnit, WindSpeedUnit


def decode_temperature(value: float, unit: TemperatureUnit) -> float:
    if unit == TemperatureUnit.CELSIUS:
        return value
    if unit == TemperatureUnit.FAHRENHEIT:
        return value * 1.8 + 32
    raise ValueError("Invalid unit")


def encode_temperature(value: float, unit: TemperatureUnit) -> float:
    if unit == TemperatureUnit.CELSIUS:
        return value
    if unit == TemperatureUnit.FAHRENHEIT:
        return (value - 32) / 1.8
    raise ValueError("Invalid unit")


def decode_speed(value: float, unit: WindSpeedUnit) -> float:
    if unit == WindSpeedUnit.M_S:
        return value
    if unit == WindSpeedUnit.KM_H:
        return value / 1000 * 3600
    if unit == WindSpeedUnit.MPH:
        return value * 2.2369363
    if unit == WindSpeedUnit.KNOTS:
        return value * 1.9438462
    raise ValueError("Invalid unit")


def encode_speed(value: float, unit: WindSpeedUnit) -> float:
    if unit == WindSpeedUnit.M_S:
        return value
    if unit == WindSpeedUnit.KM_H:
        return value / 3600 * 1000
    if unit == WindSpeedUnit.MPH:
        return value / 2.2369363
    if unit == WindSpeedUnit.KNOTS:
        return value / 1.9438462
    raise ValueError("Invalid unit")


def decode_precipitation(value: float, unit: PrecipitationUnit) -> float:
    if unit == PrecipitationUnit.MILLIMETER:
        return value
    if unit == PrecipitationUnit.INCH:
        return value * 0.0393701
    raise ValueError("Invalid unit")


def encode_precipitation(value: float, unit: PrecipitationUnit) -> float:
    if unit == PrecipitationUnit.MILLIMETER:
        return value
    if unit == PrecipitationUnit.INCH:
        return value / 0.0393701
    raise ValueError("Invalid unit")
