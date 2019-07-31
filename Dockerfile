FROM docker.beryju.org/p2/base:latest

COPY ./p2/ /app/p2
COPY ./manage.py /app/

USER p2

WORKDIR /app/
