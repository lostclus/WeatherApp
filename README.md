# WeatherApp

My pet project. Just a demo web application to demonstrate code and
technologies.

Features:
- User registration and authentication
- User settings form
- CRUD on user locations
- Query weather data on selected location
- Under the hood it will get weather data from Open-Meteo API and store it in the local database

Tech stack on backend:
- Python
- Django, FastAPI
- Celery, ARQ
- PostgreSQL, Redis, Kafka, ClickHouse

Tech stack on frontend:
- TypeScript/React
- Material UI

This project use my open source Python libraries:
- aiosafeconsumer <https://github.com/lostclus/aiosafeconsumer>
- django-kafka-streamer <https://github.com/lostclus/django-kafka-streamer>

Code quality:
- PEP8 (linted by black and ruff)
- Static typing (validated by mypy)
- Unit and integration tests (powered by pytest)

Architecture: micro services. Services:

`core`
: Core service. Stack: Django, PostgreSQL, Celery. Provides user and locations
database and REST API. Stream data to Kafka.

`loader`
: Data loader service. Stack: ARQ, Redis, Kafka. Provides asynchronous periodic
tasks to load weather data from public API and stream data to Kafka.

`query`
: Weather data query service. Stack: FastAPI, Kafka, ClickHouse. Provides
weather database and REST API.

`ui`
: User interface. Stack: TypeScript/React, Material UI.

Development plan:

- [x] Implement authorization API in `core` service
- [x] Implement authorization in UI
- [x] Implement user settings API in `core` service
- [x] Implement user settings form in UI
- [x] Implement locations API (CRUD) in `core` service
- [x] Implement locations CRUD in UI
- [x] Implement streaming data from `core` service to Kafka
- [x] Implement consumer to sync locations data in `loader` service
- [x] Implement asynchronous tasks in `loader` to get weather data from public API
  and stream it to Kafka
- [x] Implement consumer to sync weather data in `query` service
- [x] Implement weather API in `query` service
- [x] Implement weather explore page in UI
- [x] Implement weather dashboard UI
- [ ] Implement weather aggregation API
- [ ] Implement weather aggregation UI

## Local Deploy

First install Docker Compose, then type:

    docker compose build
    docker compose run --rm core-migrate
    docker compose run --rm query-migrate
    docker compose up -d
    docker compose run --rm core-stream
    docker compose run --rm loader-stream

<http://localhost:3000>
: Application user interface

<http://localhost:3000/core/admin>
: Admin interface

<http://localhost:3000/core/api/v1/docs>
: core API documentation

<http://localhost:3000/query/api/v1/docs>
: query API documentation

Go to <http://localhost:3000> and create new user (sign-up). The first user
created will have superuser privileges and can login to the admin area.

Run linters:

    make lint

Run tests:

    docker compose run --rm core-test
    docker compose run --rm loader-test
    docker compose run --rm query-test
