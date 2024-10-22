from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from weatherapp.jwtauth import JWTError

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


@app.exception_handler(JWTError)
def _auth_error_handler(request: Request, exc: JWTError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={"detail": str(exc)},
    )
