ARG PYTHON_VER=3.12.6

FROM python:$PYTHON_VER-alpine AS builder

RUN apk add --no-cache \
    build-base \
    git \
    postgresql-dev

RUN pip install --upgrade pip

WORKDIR /root

COPY ../jwtauth.lib ../jwtauth.lib
COPY ../protocol.lib ../protocol.lib
COPY core.srv/requirements.txt ./
RUN sed -i "s/^-e //" requirements.txt \
    && pip wheel --wheel-dir=/root/wheels \
    -r ./requirements.txt

FROM python:$PYTHON_VER-alpine AS base
ARG USER_ID=1000
ARG USER_GROUP_ID=1000

COPY --from=builder /root/wheels /root/wheels

RUN apk add --no-cache \
    gettext \
    libpq \
    tzdata

RUN pip install --upgrade pip

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

RUN addgroup -g $USER_GROUP_ID -S appuser \
    && adduser -u $USER_ID -G appuser -S -s /bin/sh -h /app appuser

WORKDIR /app

COPY ../jwtauth.lib ../jwtauth.lib
COPY ../protocol.lib ../protocol.lib
COPY core.srv/requirements.txt ./
RUN \
    sed -i "s|^-e ../jwtauth.lib|weatherapp.jwtauth|" requirements.txt \
    && sed -i "s|^-e ../protocol.lib|weatherapp.protocol|" requirements.txt \
    && sed -i "s/ @ git.*$//" requirements.txt \
    && pip install --no-index \
    --find-links=/root/wheels \
    -r ./requirements.txt

FROM base AS development

WORKDIR /app
USER appuser

ENV API_PORT=8000
ENV PYTHONUNBUFFERED=1

CMD python manage.py runserver 0.0.0.0:$API_PORT

FROM base AS production

WORKDIR /app

COPY core.srv/weatherapp_core ./weatherapp_core
COPY core.srv/*.py ./
COPY core.srv/pyproject.toml ./

RUN python manage.py collectstatic --noinput

USER appuser

CMD uvicorn weatherapp_core.asgi:application
