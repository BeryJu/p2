FROM golang:latest AS builder

WORKDIR /go/src/git.beryju.org/BeryJu.org/p2/tier0

ENV GO111MODULE=on
ENV GOOS=linux
ENV GOARCH=amd64
ENV CGO_ENABLED=0

COPY . .

RUN go mod download && \
    go build -ldflags "-s -w" -v -o /go/bin/tier0

FROM alpine:latest

COPY --from=builder /go/bin/tier0 /tier0

CMD "/tier0 server"
