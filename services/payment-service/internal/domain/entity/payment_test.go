package entity_test

import (
	"testing"
	"errors"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

// Testa o reembolso com todos os status de pagamento inválidos
func TestInvalidRefundWithInvalidPaymentStatus(t *testing.T) {
	user := entity.CancelByUser
	statusList := []entity.PaymentStatus{
		entity.PaymentPending,
		entity.PaymentRefunded,
		entity.PaymentFailed,
	}

	for _, status := range statusList {
		p := entity.Payment{
			ID: "1",
			OrderID: "1",
			Amount: 100,
			Status: status,
		}
	
		_, err := p.Refund(user)
	
		if !errors.Is(err, entity.ErrRefundInvalidStatus) {
			t.Errorf("Pagamentos com o status %v não podem ser reembolsados", status)
		}
	}

}

// Testa o reembolso com um usuário de cancelamento inválido
func TestInvalidRefundWithInvalidCancelUser(t *testing.T) {
	user := entity.CancelUser("USUARIO_INVALIDO")
	p := entity.Payment{
		ID: "1",
		OrderID: "1",
		Amount: 100,
		Status: entity.PaymentApproved,
	}

	_, err := p.Refund(user)

	if !errors.Is(err, entity.ErrRefundInvalidUser) {
		t.Errorf("Pagamentos com usuários de cancelamento diferentes de USER e STORE são inválidos")
	}
}

// Testa o reembolso de pagamento cancelado por parte do usuário
func TestValidRefundWithUserCancelUser(t *testing.T) {
	user := entity.CancelByUser
	p := entity.Payment{
		ID: "1",
		OrderID: "1",
		Amount: 100,
		Status: entity.PaymentApproved,
	}

	refundAmount, err := p.Refund(user)

	if err != nil {
		t.Fatalf("Erro inesperado: %v", err)
	}

	if (refundAmount != (100 * 0.7)) {
		t.Errorf("O valor de reembolsos de pagamentos cancelados por usuários deve ser de 70%% do valor total")
	}
}

// Testa o reembolso de pagamento cancelado por parte da loja
func TestValidRefundWithStoreCancelUser(t *testing.T) {
	user := entity.CancelByStore
	p := entity.Payment{
		ID: "1",
		OrderID: "1",
		Amount: 100,
		Status: entity.PaymentApproved,
	}

	refundAmount, err := p.Refund(user)

	if err != nil {
		t.Fatalf("Erro inesperado: %v", err)
	}

	if refundAmount != 100 {
		t.Errorf("Pagamentos cancelados pela loja devem ser reembolsados em seu valor total")
	}
}


// Testa o pagamento com todos os status de pagamento inválidos
func TestInvalidProcessWithInvalidPaymentStatus(t *testing.T) {
	statusList := []entity.PaymentStatus{
		entity.PaymentApproved,
		entity.PaymentRefunded,
		entity.PaymentFailed,
	}

	for _, status := range statusList {
		p := entity.Payment{
			ID: "1",
			OrderID: "1",
			Amount: 100,
			Method: entity.MethodCredit,
			Status: status,
		}
	
		err := p.Process()
	
		if !errors.Is(err, entity.ErrPaymentInvalidStatus) {
			t.Errorf("Pagamentos com o status %v não podem ser realizados", status)
		}
	}

}

func TestInvalidProcessWithInvalidValue(t *testing.T) {
	p := entity.Payment{
			ID: "1",
			OrderID: "1",
			Amount: 0,
			Method: entity.MethodCredit,
			Status: entity.PaymentPending,
		}
	
		err := p.Process()
	
		if !errors.Is(err, entity.ErrPaymentInvalidValue) {
			t.Errorf("Pagamentos com valores menores ou iguais a zero não podem ser realizados")
		}
}

func TestValidProcess(t *testing.T) {
	p := entity.Payment{
			ID: "1",
			OrderID: "1",
			Amount: 100,
			Method: entity.MethodCredit,
			Status: entity.PaymentPending,
		}
	
		err := p.Process()

		if err != nil {
			t.Fatalf("Erro inesperado: %v", err)
		}

		if p.Status != entity.PaymentApproved {
			t.Errorf("Deve ser possível processar pagamentos que estejam pendentes e com valor superior a zero")
		}
}