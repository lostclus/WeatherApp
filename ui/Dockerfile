ARG NODE_VER=20.17

FROM node:$NODE_VER-alpine AS builder
ARG USER_ID=1000
ARG USER_GROUP_ID=1000

RUN deluser node \
    && addgroup -g $USER_GROUP_ID -S appuser \
    && adduser -u $USER_ID -G appuser -S -s /bin/sh -h /app appuser

WORKDIR /app
USER appuser
COPY --chown=appuser ui/package*.json ui/yarn.lock /app
RUN npm install

FROM node:$NODE_VER-alpine AS base
ARG USER_ID=1000
ARG USER_GROUP_ID=1000

COPY --from=builder /app/node_modules /app/node_modules

RUN deluser node \
    && addgroup -g $USER_GROUP_ID -S appuser \
    && adduser -u $USER_ID -G appuser -S -s /bin/sh -h /app appuser

RUN mkdir -p /app/node_modules/.vite && chown appuser: /app/node_modules/.vite

WORKDIR /app
USER appuser

COPY ui/.* /app
COPY ui/*.json /app
COPY ui/*.html /app
COPY ui/*.ts /app

FROM base AS development
CMD npm run dev
ENV NODE_ENV=development

FROM base AS production
ENV NODE_ENV=production

COPY ui/public /app/public
COPY ui/src /app/src

CMD npm run start
