package rabbitmq

import (
	"encoding/json"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

type Publisher struct {
	channel *amqp.Channel
}

func NewPublisher(ch *amqp.Channel) *Publisher {
	return &Publisher{channel: ch}
}

func (p *Publisher) Publish(queue string, body any) error {
	payload, err := json.Marshal(body)
	if err != nil {
		return err
	}

	err = p.channel.Publish(
		"", queue, false, false, 
		amqp.Publishing{
			ContentType: "application/json",
			DeliveryMode: amqp.Persistent,
			Body: payload,
		},
	)

	if err != nil {
		log.Fatalf("Erro ao publicar na fila \"%v\": %v", queue, err)
	}

	log.Printf("Evento publicado na fila \"%v\"", queue)
	return nil
}