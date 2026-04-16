package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

type usecase struct {
	repo PaymentRepository
}

func (u *usecase) RefundPayment(
	ctx context.Context,
	input RefundPaymentInput,
) (RefundPaymentOutput, error) {

	p, error := u.repo.FindByID(ctx, input.PaymentID)

	if err != nil {
		return RefundPaymentOutput{}, err
	}

	refundedAmount, err := p.Refund(input.CancelUser)

	if err != nill {
		return RefundPaymentOutput{}, err
	}

	err := u.repo.Save(ctx, *p)

	if err != nil {
		return ProcessPaymentOutput{}, err
	}

	return RefundPaymentOutput{
		RefundedAmount: refundedAmount,
		Status: p.Status
	}, nil
}