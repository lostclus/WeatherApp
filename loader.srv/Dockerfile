ARG PYTHON_VER=3.12.6

FROM python:$PYTHON_VER-alpine AS builder

RUN apk add --no-cache \
    build-base \
    g++ \
    gcc \
    git \
    musl-dev \
    zlib-dev

RUN pip install --upgrade pip

WORKDIR /root

COPY ../protocol.lib ../protocol.lib
COPY loader.srv/requirements.txt ./
RUN sed -i "s/^-e //" requirements.txt \
    && pip wheel --wheel-dir=/root/wheels \
    -r ./requirements.txt

FROM python:$PYTHON_VER-alpine AS base
ARG USER_ID=1000
ARG USER_GROUP_ID=1000

COPY --from=builder /root/wheels /root/wheels

RUN apk add --no-cache \
    gettext \
    tzdata

RUN pip install --upgrade pip

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

RUN addgroup -g $USER_GROUP_ID -S appuser \
    && adduser -u $USER_ID -G appuser -S -s /bin/sh -h /app appuser

WORKDIR /app

COPY ../protocol.lib ../protocol.lib
COPY loader.srv/requirements.txt ./
RUN \
    sed -i "s|^-e ../protocol.lib|weatherapp.protocol|" requirements.txt \
    && sed -i "s/ @ git.*$//" requirements.txt \
    && pip install --no-index \
    --find-links=/root/wheels \
    -r ./requirements.txt

FROM base AS development

WORKDIR /app
USER appuser

ENV API_PORT=8000
ENV PYTHONUNBUFFERED=1

CMD python -m aiosafeconsumer.run --pool-settings=weatherapp_loader.consumers.init

FROM base AS production

WORKDIR /app

COPY loader.srv/weatherapp_loader ./weatherapp_loader
COPY loader.srv/*.py ./
COPY loader.srv/pyproject.toml ./

RUN python manage.py collectstatic --noinput

USER appuser

CMD python -m aiosafeconsumer.run --pool-settings=weatherapp_loader.consumers.init
