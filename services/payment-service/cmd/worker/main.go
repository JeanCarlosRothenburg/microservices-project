package main

import (
	"database/sql"
	"log"
	"os"

	"github.com/JeanCarlosRothenburg/payment-service/internal/infrastructure/messaging/rabbitmq"
	"github.com/JeanCarlosRothenburg/payment-service/internal/infrastructure/repository"
	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"
	_ "github.com/lib/pq"
)

func main() {
	conn := rabbitmq.NewConnection()
	defer conn.Close()

	db, err := sql.Open("postgres", os.Getenv("POSTGRES_DB_URL"))
	if err != nil {
		log.Fatalf("Falha ao estabelecer conexão com o DB: %v", err)
	}
	defer db.Close()

	repo := repository.NewPaymentRepository(db)
	uc := payment.NewUseCase(repo)

	rabbitmq.NewConsumer(conn.Channel(), uc).Start()
}
