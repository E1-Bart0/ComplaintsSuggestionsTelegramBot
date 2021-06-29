FROM python:3.9-buster
WORKDIR /app

COPY ./.requirements /.requirements
COPY bot/db/alembic.ini .

RUN pip install --no-cache-dir -r /.requirements/common.txt

RUN useradd bot


COPY ./.scripts .
COPY ./bot /app

RUN chown -R bot:bot /app
USER bot
