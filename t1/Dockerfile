FROM golang:latest AS builder

WORKDIR /go/src/git.beryju.org/BeryJu.org/t1

ENV GO111MODULE=on

COPY go.mod .
COPY go.sum .

RUN go mod download && \
    go build -v -o /go/bin/t1

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /go/bin/t1 /t1

CMD "/t1"
