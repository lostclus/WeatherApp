import logging.config
import os
from typing import Any

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherapp_core.settings")


@setup_logging.connect  # type: ignore
def setup_logging_handler(**kwargs: Any) -> None:
    from django.conf import settings

    logging.config.dictConfig(settings.LOGGING)


app = Celery("weatherapp_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
