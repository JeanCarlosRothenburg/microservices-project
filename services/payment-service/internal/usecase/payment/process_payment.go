package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

type usecase struct {
	repo PaymentRepository
}

func (u *usecase) ProcessPayment(
	ctx context.Context,
	input ProcessPaymentInput,
) (ProcessPaymentOutput, error) {
	p := entity.Payment{
		ID: generateID(),
		OrderID: input.OrderID,
		Amount: input.Amount,
		Method: input.Method,
		Status: entity.PaymentPending,
	}

	isPaid, err := p.Process()

	if err != nil {
		return ProcessPaymentOutput{}, err
	}

	if !isPaid {
		return ProcessPaymentOutput{}, err
	}

	err := u.repo.Save(ctx, *p)

	if err != nil {
		return ProcessPaymentOutput{}, err
	}

	return ProcessPaymentOutput{
		PaymentID: p.ID,
		Status: p.Status
	}, nil
}