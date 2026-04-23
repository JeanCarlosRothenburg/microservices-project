# Test Stage
FROM golang:1.26.2-alpine AS test

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go test ./... --cover

# Build Stage
FROM golang:1.26.2-alpine AS build

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o app ./cmd/worker

# Runtime Stage
FROM golang:1.26.2-alpine

WORKDIR /app

COPY --from=build /app/app .

RUN apk add --no-cache ca-certificates

CMD ["./app"]