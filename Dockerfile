FROM python:3.6-slim-stretch as build

COPY ./p2/ /app/p2
COPY ./manage.py /app/
COPY ./requirements.txt /app/

WORKDIR /app/

RUN apt-get update && apt-get install build-essential libffi-dev libsasl2-dev python-dev libldap2-dev libssl-dev libpq-dev -y && \
    mkdir /app/static/ && \
    pip install -r requirements.txt && \
    pip install psycopg2 && \
    ./manage.py collectstatic --no-input && \
    apt-get remove --purge -y build-essential && \
    apt-get autoremove --purge -y

FROM python:3.6-alpine

COPY ./p2/ /app/p2
COPY --from=build /app/static /app/static/
COPY ./manage.py /app/
COPY ./requirements.txt /app/

RUN apk update && \
    apk add --no-cache openssl-dev libffi-dev libmagic libffi-dev build-base jpeg libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev openldap-dev postgresql-dev && \
    pip install -r /app/requirements.txt  --no-cache-dir && \
    apk del openssl-dev libffi-dev libffi-dev build-base libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl jpeg-dev zlib-dev freetype-dev lcms2-dev tk-dev tcl-dev postgresql-dev && \
    adduser -S p2 && \
    chown -R p2 /app

USER p2

WORKDIR /app/
