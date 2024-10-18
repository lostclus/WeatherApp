from fastapi import FastAPI

from ..logging import configure_logging, configure_sentry
from .weather import router as weather_router

configure_logging()
configure_sentry()

app = FastAPI(root_path="/query/api/v1")
app.include_router(weather_router)
