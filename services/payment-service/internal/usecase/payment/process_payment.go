package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

func generateID() string {
	return "payment-123"
}

func (u *usecase) ProcessPayment(
	ctx context.Context,
	input ProcessPaymentInput,
) (ProcessPaymentOutput, error) {
	p := entity.Payment{
		ID: generateID(),
		OrderID: input.OrderID,
		Amount: input.Amount,
		Method: entity.PaymentMethod(input.Method),
		Status: entity.PaymentPending,
	}

	err := p.Process()

	if err != nil {
		return ProcessPaymentOutput{}, err
	}

	err = u.repo.Save(ctx, p)
 
	if err != nil {
		return ProcessPaymentOutput{}, err
	}

	return ProcessPaymentOutput{
		PaymentID: p.ID,
		Status: string(p.Status),
	}, nil
}