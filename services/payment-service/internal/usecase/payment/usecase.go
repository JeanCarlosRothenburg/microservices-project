package payment

import "github.com/JeanCarlosRothenburg/payment-service/internal/domain/repository"

type usecase struct {
	repo repository.PaymentRepository
}

func NewUseCase(repo repository.PaymentRepository) UseCase {
	return &usecase{
		repo: repo,
	}
}