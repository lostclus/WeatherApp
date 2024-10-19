from fastapi import FastAPI

from .. import __version__
from ..logging import configure_logging, configure_sentry
from .weather import router as weather_router

configure_logging()
configure_sentry()

app = FastAPI(
    title="WeatherApp Data Query API",
    root_path="/query/api/v1",
    version=__version__,
)
app.include_router(weather_router)
