import asyncio
import os
import sys

import arq
from arq.typing import WorkerSettingsBase

from ..logging import configure_logging, configure_sentry
from .arq import func_path, get_arq_pool
from .weather import stream_weather_location_task, stream_weather_task


class WorkerSettings(WorkerSettingsBase):
    functions = [
        arq.func(func_path(stream_weather_location_task)),
        arq.func(func_path(stream_weather_task)),
    ]
    cron_jobs = [
        arq.cron(
            func_path(stream_weather_task),
            minute=5,
        ),
    ]
    max_jobs = 4


def main() -> int:
    configure_logging()
    configure_sentry()

    loop = asyncio.get_event_loop()

    workers = [
        arq.worker.create_worker(
            settings_cls=WorkerSettings,
            redis_pool=get_arq_pool(),
        ),
    ]

    try:
        loop.run_until_complete(asyncio.gather(*[wrk.async_run() for wrk in workers]))
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        loop.run_until_complete(asyncio.gather(*[wrk.close() for wrk in workers]))
    loop.close()

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
