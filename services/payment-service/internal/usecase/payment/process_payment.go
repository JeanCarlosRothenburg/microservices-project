package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

func (u *usecase) ProcessPayment(
	ctx context.Context,
	input ProcessPaymentInput,
) (ProcessPaymentOutput, error) {
	p := entity.Payment{
		OrderID: input.OrderID,
		Amount:  input.Amount,
		Method:  entity.PaymentMethod(input.Method),
		Status:  entity.PaymentPending,
	}

	err := p.Process()

	if err != nil {
		return ProcessPaymentOutput{
			OrderID: p.OrderID,
			Status:  string(entity.PaymentFailed),
		}, err
	}

	p, err = u.repo.Save(ctx, p)

	if err != nil {
		return ProcessPaymentOutput{
			PaymentID: p.ID,
			OrderID:   p.OrderID,
			Status:    string(p.Status),
		}, err
	}

	return ProcessPaymentOutput{
		PaymentID: p.ID,
		OrderID:   p.OrderID,
		Status:    string(p.Status),
	}, nil
}
