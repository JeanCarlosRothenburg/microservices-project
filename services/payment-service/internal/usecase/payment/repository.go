package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

type PaymentRepository interface {
	Save(ctx context.Context, payment entity.Payment) error
	FindByID(ctx context.Context, ID string) (*entity.Payment, error)
}