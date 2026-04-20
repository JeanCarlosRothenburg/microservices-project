package payment

import (
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

func (u *usecase) RefundPayment(
	ctx context.Context,
	input RefundPaymentInput,
) (RefundPaymentOutput, error) {

	p, err := u.repo.FindByID(ctx, input.PaymentID)

	if err != nil {
		return RefundPaymentOutput{}, err
	}

	refundedAmount, err := p.Refund(entity.CancelUser(input.CancelUser))

	if err != nil {
		return RefundPaymentOutput{}, err
	}

	err = u.repo.Save(ctx, *p)

	if err != nil {
		return RefundPaymentOutput{}, err
	}

	return RefundPaymentOutput{
		RefundedAmount: refundedAmount,
		Status: string(p.Status),
	}, nil
}