FROM python:3.9-slim as base
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y curl build-essential

COPY . .
RUN curl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py > get-poetry

RUN python get-poetry

ENV PATH = "${PATH}:/root/.poetry/bin"

RUN poetry config virtualenvs.create false

FROM base as dev
RUN apt-get install -y git
RUN poetry install

FROM base as prod
RUN poetry install --no-dev
