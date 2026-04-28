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
		return RefundPaymentOutput{
			PaymentID:      p.ID,
			OrderID:        p.ID,
			RefundedAmount: refundedAmount,
			Status:         string(p.Status),
		}, err
	}

	savedP, err := u.repo.Save(ctx, *p)
	p = &savedP

	if err != nil {
		return RefundPaymentOutput{
			PaymentID:      p.ID,
			OrderID:        p.OrderID,
			RefundedAmount: refundedAmount,
			Status:         string(p.Status),
		}, err
	}

	return RefundPaymentOutput{
		PaymentID:      p.ID,
		OrderID:        p.OrderID,
		RefundedAmount: refundedAmount,
		Status:         string(p.Status),
	}, nil
}
