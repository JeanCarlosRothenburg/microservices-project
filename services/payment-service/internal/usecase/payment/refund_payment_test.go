package payment_test

import (
	"context"
	"errors"
	"testing"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
	"github.com/JeanCarlosRothenburg/payment-service/internal/usecase/payment"
)

// Testa o processamento de reembolso com um pagamento inexistente
func TestRefundProcessWithNonExistentPayment(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		FindFunc: func(id string) (*entity.Payment, error) {
			return nil, payment.ErrPaymentNotFound
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.RefundPaymentInput{
		PaymentID:  "",
		CancelUser: string(entity.CancelByStore),
	}

	_, err := uc.RefundPayment(ctx, input)

	if !errors.Is(err, payment.ErrPaymentNotFound) {
		t.Fatalf("Era esperado o erro ErrPaymentNotFound, porém foi disparado o errro: %v", err)
	}
}

// Testa o processamento do reembolso com um usuário de cancelamento inválido
func TestRefundProcessWithInvalidCancelUser(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		FindFunc: func(id string) (*entity.Payment, error) {
			return &entity.Payment{
				ID:      "1",
				OrderID: "1",
				Amount:  100,
				Method:  entity.MethodCredit,
				Status:  entity.PaymentApproved,
			}, nil
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.RefundPaymentInput{
		PaymentID:  "1",
		CancelUser: string(entity.CancelUser("USUARIO_INVALIDO")),
	}

	_, err := uc.RefundPayment(ctx, input)

	if !errors.Is(err, entity.ErrRefundInvalidUser) {
		t.Fatalf("Era esperado o erro ErrRefundInvalidUser, porém foi disparado o errro: %v", err)
	}
}

// Testa o processamento do reembolso com erro no salvamento dos dados
func TestRefundProcessWithErrorOnSave(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		SaveFunc: func(p entity.Payment) (entity.Payment, error) {
			return p, errors.New("Teste de erro no salvamento")
		},
		FindFunc: func(id string) (*entity.Payment, error) {
			return &entity.Payment{
				ID:      "1",
				OrderID: "1",
				Amount:  100,
				Method:  entity.MethodCredit,
				Status:  entity.PaymentApproved,
			}, nil
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.RefundPaymentInput{
		PaymentID:  "1",
		CancelUser: string(entity.CancelByStore),
	}

	_, err := uc.RefundPayment(ctx, input)

	if err == nil {
		t.Fatalf("Era esperado erro ao salvar o registro, porém não foi disparado")
	} else if err.Error() != "Teste de erro no salvamento" {
		t.Fatalf("Era o erro \"Teste de erro no salvamento\" ao salvar o registro, porém foi disparado o erro: %v", err)
	}
}

// Testa o processamento do reembolso para pagamento válido cancelado pela loja
func TestRefundProcessForPaymentCanceledByStore(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		FindFunc: func(id string) (*entity.Payment, error) {
			return &entity.Payment{
				ID:      "1",
				OrderID: "1",
				Amount:  100,
				Method:  entity.MethodCredit,
				Status:  entity.PaymentApproved,
			}, nil
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.RefundPaymentInput{
		PaymentID:  "1",
		CancelUser: string(entity.CancelByStore),
	}

	response, _ := uc.RefundPayment(ctx, input)
	expectedRefund := 100.0

	if response.RefundedAmount != expectedRefund {
		t.Fatalf("Era esperado reembolso total do valor de R$ %v, porém foi reembolsado apenas %v", expectedRefund, response.RefundedAmount)
	}
}

// Testa o processamento do reembolso para pagamento válido cancelado por parte do usuário
func TestRefundProcessForPaymentCanceledByUser(t *testing.T) {
	ctx := context.Background()
	repo := &payment.PaymentRepositoryMock{
		FindFunc: func(id string) (*entity.Payment, error) {
			return &entity.Payment{
				ID:      "1",
				OrderID: "1",
				Amount:  100,
				Method:  entity.MethodCredit,
				Status:  entity.PaymentApproved,
			}, nil
		},
	}
	uc := payment.NewUseCase(repo)
	input := payment.RefundPaymentInput{
		PaymentID:  "1",
		CancelUser: string(entity.CancelByUser),
	}

	response, _ := uc.RefundPayment(ctx, input)
	expectedRefund := 100 * 0.7

	if response.RefundedAmount != expectedRefund {
		t.Fatalf("Era esperado reembolso no valor de R$ %v, porém foi reembolsado %v", expectedRefund, response.RefundedAmount)
	}
}
