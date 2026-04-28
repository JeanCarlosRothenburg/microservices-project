package payment

// DTOs de processamento de pagamento
type ProcessPaymentInput struct {
	OrderID string  `json:"order_id"`
	Amount  float64 `json:"valor_total"`
	Method  string  `json:"metodo_pagamento"`
}

type ProcessPaymentOutput struct {
	PaymentID string
	OrderID   string
	Status    string
}

// DTOs de reembolso de pagamento
type RefundPaymentInput struct {
	PaymentID  string
	CancelUser string
}

type RefundPaymentOutput struct {
	PaymentID      string
	OrderID        string
	RefundedAmount float64
	Status         string
}
