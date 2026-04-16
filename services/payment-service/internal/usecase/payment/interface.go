package payment

import "context"

type UseCase interface {
	ProcessPayment(ctx context.Context, input ProcessPaymentInput) (ProcessPaymentOutput, error)
	RefundPayment(ctx context.Context, input RefundPaymentInput) (RefundPaymentOutput, error)
}