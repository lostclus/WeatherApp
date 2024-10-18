from fastapi import FastAPI

from ..logging import configure_logging, configure_sentry

configure_logging()
configure_sentry()

app = FastAPI()
