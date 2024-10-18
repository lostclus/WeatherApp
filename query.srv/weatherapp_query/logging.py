import logging.config

import sentry_sdk

from .settings import settings


def configure_sentry() -> None:
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.sentry_environment or None,
        )


def configure_logging() -> None:
    logging.config.dictConfig(settings.logging)
