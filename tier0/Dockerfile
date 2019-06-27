FROM golang:latest AS builder

WORKDIR /go/src/git.beryju.org/BeryJu.org/p2/tier0

ENV GO111MODULE=on

COPY go.mod .
COPY go.sum .

RUN go mod download && \
    go build -v -o /go/bin/tier0

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /go/bin/tier0 /tier0

CMD "/tier0"
