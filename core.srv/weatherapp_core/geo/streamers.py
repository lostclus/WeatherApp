from kafkastreamer import Streamer, register

from .models import Location


@register(Location)
class LocationStreamer(Streamer):
    topic = "locations"
