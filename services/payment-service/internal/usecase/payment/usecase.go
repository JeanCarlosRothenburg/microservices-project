package payment

type usecase struct {
	repo PaymentRepository
}

func NewUseCase(repo PaymentRepository) UseCase {
	return &usecase{
		repo: repo,
	}
}