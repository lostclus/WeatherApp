from kafkastreamer import Streamer, register

from .models import User


@register(User)
class UserStreamer(Streamer):
    topic = "users"
    exclude = ("password",)
