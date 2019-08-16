FROM python:3.7-alpine as builder

WORKDIR /mkdocs

COPY docs/ docs
COPY mkdocs.yml .

RUN apk add git && \
    pip install mkdocs && \
    pip install git+https://github.com/BeryJu/mkdocs-bootstrap4.git && \
    mkdocs build

FROM nginx

COPY --from=builder /mkdocs/site /usr/share/nginx/html
