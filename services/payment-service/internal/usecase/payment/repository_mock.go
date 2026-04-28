package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

// Define o modelo para o mock do repositório
type PaymentRepositoryMock struct {
	SaveFunc func(entity.Payment) (entity.Payment, error)
	FindFunc func(ID string) (*entity.Payment, error)
}

// Método de salvamento do mock do repositório
func (mock *PaymentRepositoryMock) Save(ctx context.Context, p entity.Payment) (entity.Payment, error) {
	if mock.SaveFunc != nil {
		return mock.SaveFunc(p)
	}

	return p, nil
}

// Método de busca por ID do mock do repositório
func (mock *PaymentRepositoryMock) FindByID(ctx context.Context, id string) (*entity.Payment, error) {
	if mock.FindFunc != nil {
		return mock.FindFunc(id)
	}

	return nil, nil
}
