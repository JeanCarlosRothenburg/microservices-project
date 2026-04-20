package main

import (
	"context"
	"log"

	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"
)

 func main() {
	ctx := context.Background()
	// TODO: implementar repositório do BD
	repo := payment.PaymentRepositoryMock{}
	uc := payment.NewUseCase(repo)

	for {
		// Evento recebido do RabbitMQ
	}
	 
}