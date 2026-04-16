func NewUseCase(repo PaymentReository) UseCase {
	return &usecase{
		repo: repo,
	}
}