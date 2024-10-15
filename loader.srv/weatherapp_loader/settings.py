import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(
    ","
)

REDIS_QUEUE_URL = os.getenv("REDIS_QUEUE_URL", "redis://localhost:6379/1")
REDIS_STORAGE_URL = os.getenv("REDIS_STORAGE_URL", "redis://localhost:6379/2")

_logging_handlers = os.getenv("LOGGING_HANDLERS", "console,worker_console").split(",")
_logging_level = os.getenv("LOGGING_LEVEL", "DEBUG")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "context_injecting": {
            "()": "aiosafeconsumer.logging.ContextInjectingFilter",
        },
        "is_worker_context": {
            "()": "aiosafeconsumer.logging.IsWorkerContextFilter",
        },
        "is_not_worker_context": {
            "()": "aiosafeconsumer.logging.IsWorkerContextFilter",
            "invert": True,
        },
    },
    "formatters": {
        "common": {
            "format": "[%(levelname)s/%(name)s] %(message)s",
        },
        "worker": {
            "()": "aiosafeconsumer.logging.ExtraFieldsFormatter",
            "fmt": "[%(levelname)s/%(worker_type)s-%(worker_id)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "common",
            "filters": ["is_not_worker_context"],
        },
        "worker_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "worker",
            "filters": ["is_worker_context", "context_injecting"],
        },
    },
    "loggers": {
        "aiosafeconsumer": {
            "level": "DEBUG",
            "handlers": _logging_handlers,
            "propagate": True,
        },
        "weatherapp": {
            "level": "DEBUG",
            "handlers": _logging_handlers,
            "propagate": True,
        },
        "weatherapp_loader": {
            "level": "DEBUG",
            "handlers": _logging_handlers,
            "propagate": True,
        },
    },
}

SENTRY_DSN = os.getenv("SENTRY_DSN", "")
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "")
