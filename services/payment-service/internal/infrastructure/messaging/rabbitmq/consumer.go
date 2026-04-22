package rabbitmq

import (
	"context"
	"encoding/json"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"	
)

type Consumer struct {
	channel *amqp.Channel
	paymentUC payment.UseCase
	publisher *Publisher
}

func NewConsumer(ch *amqp.Channel, uc payment.UseCase) *Consumer {
	return &Consumer{
		channel: ch,
		paymentUC: uc,
		publisher: NewPublisher(ch),
	}
}

func (c *Consumer) Start() {
	msgs, err := c.channel.Consume(
		"payment.queue", "", false, false, false, false, nil,
	)

	if err != nil {
		log.Fatalf("Erro ao registrar consumer: %v", err)
	}

	log.Println("Payment-Service: aguardando mensagens...")

	for msg := range msgs {
		c.handle(msg)
	}
}

func (c *Consumer) handle(msg amqp.Delivery) {
	var input payment.ProcessPaymentInput

	err := json.Unmarshal(msg.Body, &input)

	if err != nil {
		log.Printf("Falha ao converter o JSON recebido: %v", err)
		msg.Nack(false, false)
		return
	}

	output, err = c.paymentUC.ProcessPayment(context.Background(), input)
	if err != nil {
		log.Printf("Erro ao processar pagamento: %v", err)
		msg.Nack(false, true)
		return
	}

	err = c.publisher.Publish(output.Status, output)
	if err != nil {
		log.Printf("Erro ao publicar o resultado do pagamento do pedido %v: %v", input.OrderID, err)
		msg.Nack(false, true)
		return
	}

	msg.Ack(false)
}
