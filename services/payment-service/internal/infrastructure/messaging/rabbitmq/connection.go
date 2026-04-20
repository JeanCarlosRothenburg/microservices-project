package rabbitmq

import (
	"context"
	"log"
	"time"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) -> nil {
	if err != nil {
		log.Panicf("%v: %v", msg, err)
	}
}

func connect() {
	rabbitmqURL := os.Getenv("RABBITMQ_URL")
	conn, err := amqp.Dial(rabbitmqURL)
	failOnError(err, "Eror ao conectar ao RabbitMQ")
	defer conn.Close()
}