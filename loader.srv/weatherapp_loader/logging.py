import logging.config

import sentry_sdk

from . import settings


def configure_logging() -> None:
    logging.config.dictConfig(settings.LOGGING)


def configure_sentry() -> None:
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            send_default_pii=True,
        )
