package main

import (
	"github.com/JeanCarlosRothenburg/payment-service/internal/infrastructure/messaging/rabbitmq"
	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"
)

 func main() {
	conn := rabbitmq.NewConnection()
	defer conn.Close()

	// TODO: implementar repositório do BD
	repo := &payment.PaymentRepositoryMock{}
	uc := payment.NewUseCase(repo)

	rabbitmq.NewConsumer(conn.Channel(), uc).Start()
}