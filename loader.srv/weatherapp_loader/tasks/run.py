import asyncio
from collections.abc import Callable
from datetime import date
from typing import Any

import click

from ..types import OpenMeteoDataset
from .arq import close_redis_pool, func_path, get_arq_pool
from .weather import stream_weather_task


async def run_task(func: Callable, **kwargs: Any) -> str:
    try:
        async with get_arq_pool() as pool:
            job = await pool.enqueue_job(func_path(func), **kwargs)
            assert job is not None
            return job.job_id
    finally:
        await close_redis_pool()


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("start_date", required=False)
@click.argument("end_date", required=False)
@click.option("--location", "-l", type=int, multiple=True)
@click.option("--dataset", type=click.Choice(list(OpenMeteoDataset)))
def stream_weather(
    start_date: str | None,
    end_date: str | None,
    location: list[int] | None,
    dataset: str | None,
) -> None:
    _start_date = start_date and date.fromisoformat(start_date) or None
    _end_date = end_date and date.fromisoformat(end_date) or None
    _location_ids = location
    _dataset = dataset and OpenMeteoDataset(dataset) or None

    job_id = asyncio.run(
        run_task(
            stream_weather_task,
            start_date=_start_date,
            end_date=_end_date,
            location_ids=_location_ids,
            dataset=_dataset,
        ),
    )
    print(f"Job: {job_id}")


if __name__ == "__main__":
    cli()
