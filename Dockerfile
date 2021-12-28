FROM python:3.9-slim
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
RUN poetry install --no-dev

CMD ['flask', 'db', 'upgrade']
