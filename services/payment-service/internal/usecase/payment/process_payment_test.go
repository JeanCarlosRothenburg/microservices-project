package payment_test

import (
	"context"
	"errors"
	"testing"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"
)

// Testa o processamento de pagamento válido
func TestValidProcessPayment(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		SaveFunc: func(p entity.Payment) (entity.Payment, error) {
			return p, nil
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.ProcessPaymentInput{
		OrderID: "1",
		Amount:  100,
		Method:  string(entity.MethodDebit),
	}

	_, err := uc.ProcessPayment(ctx, input)

	if err != nil {
		t.Fatalf("Erro em pagamento válido: %v", err)
	}
}

// Testa o processamento do pagamento com erro no pagamento
func TestInvalidProcessPayment(t *testing.T) {
	ctx := context.Background()
	uc := payment.NewUseCase(&payment.PaymentRepositoryMock{})
	input := payment.ProcessPaymentInput{
		OrderID: "1",
		Amount:  0,
		Method:  string(entity.MethodDebit),
	}

	_, err := uc.ProcessPayment(ctx, input)

	if err == nil {
		t.Fatalf("Pagamento inválido processado sem validação")
	}
}

// Testa o processamento do pagamento com sucesso no pagamento e erro no salvamento dos dados
func TestValidProcessPaymentWithErrorOnSave(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		SaveFunc: func(p entity.Payment) (entity.Payment, error) {
			return p, errors.New("Teste de erro no salvamento")
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.ProcessPaymentInput{
		OrderID: "1",
		Amount:  100,
		Method:  string(entity.MethodDebit),
	}

	_, err := uc.ProcessPayment(ctx, input)

	if err == nil {
		t.Fatalf("Erro no salvamento dos dados não identificado")
	}
}
