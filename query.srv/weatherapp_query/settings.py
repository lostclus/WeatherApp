from typing import Any

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_url: str = "http://localhost:8123"
    clickhouse_database: str = "weatherapp_query"
    clickhouse_user: str = "default"
    clickhouse_password: str = ""

    # Logging
    logging_handlers: list[str] = ["console"]
    logging_level: str = "DEBUG"

    sentry_dsn: str = ""
    sentry_environment: str = ""

    @computed_field  # type: ignore
    @property
    def logging(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "file": {
                    "format": "[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": self.logging_level,
                    "class": "logging.StreamHandler",
                    "formatter": "file",
                },
            },
            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
                "weatherapp": {
                    "level": "DEBUG",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
                "weatherapp_query": {
                    "level": "DEBUG",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
            },
        }


settings = Settings()
