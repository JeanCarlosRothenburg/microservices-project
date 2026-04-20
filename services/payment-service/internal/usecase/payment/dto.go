package payment

// DTOs de processamento de pagamento
type ProcessPaymentInput struct {
	OrderID string
	Amount float64
	Method string
}

type ProcessPaymentOutput struct {
	PaymentID string
	Status string
}


// DTOs de reembolso de pagamento
type RefundPaymentInput struct {
	PaymentID string
	CancelUser string
}

type RefundPaymentOutput struct {
	RefundedAmount float64
	Status string
}