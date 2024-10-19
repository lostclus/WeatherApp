# WeatherApp

My pet project.

Tech stack on backend:
- Python
- Django, FastAPI
- Celery, ARQ
- PostgreSQL, Redis, Kafka, ClickHouse

Tech stack on frontend:
- TypeScript/React
- Material UI

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
- [ ] Implement weather API in `query` service
- [ ] Implement weather explore page in UI

## Local Deploy

First install Docker Compose, then type:

    docker compose build
    docker compose up -d

<http://localhost:3000>
: Application user interface

<http://localhost:3000/core/admin>
: Admin interface

<http://localhost:3000/core/api/v1/docs>
: core API documentation

<http://localhost:3000/query/api/v1/docs>
: query API documentation

Run linters:

    make lint

Run tests:

    docker compose run --rm core-test
    docker compose run --rm loader-test
    docker compose run --rm query-test
