# Test Stage
FROM golang:alpine3.22 AS test

WORKDIR /app

COPY go.mod ./

RUN go get github.com/rabbitmq/amqp091-go

COPY . .

RUN go test ./... --cover

# Build Stage
FROM golang:alpine3.22 AS build

WORKDIR /app

COPY go.mod ./

RUN go get github.com/rabbitmq/amqp091-go

COPY . .

RUN go build -o app ./cmd/worker