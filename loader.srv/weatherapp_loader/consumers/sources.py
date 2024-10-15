from aiosafeconsumer.kafka import KafkaSource, KafkaSourceSettings

from ..types import Location


class LocationsSourceSettings(KafkaSourceSettings[Location]):
    pass


class LocationsSource(KafkaSource[Location]):
    settings: LocationsSourceSettings
