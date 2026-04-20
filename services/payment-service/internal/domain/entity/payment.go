package entity
 
import "errors"

type PaymentStatus string
type PaymentMethod string
type CancelUser string

const (
	// Status do pedido
	PaymentPending   PaymentStatus = "PENDENTE"
	PaymentApproved  PaymentStatus = "APROVADO"
	PaymentRefunded  PaymentStatus = "REEMBOLSADO"
	PaymentFailed    PaymentStatus = "RECUSADO"

	// Métodos de pagamento
	MethodDebit  PaymentMethod = "DEBITO"
	MethodCredit PaymentMethod = "CREDIT"
	MethodPix    PaymentMethod = "PIX"

	// Usuário de cancelamento
	CancelByUser  CancelUser = "USUARIO"
	CancelByStore CancelUser = "LOJA"
)

var (
	ErrRefundInvalidStatus           = errors.New("Somente pagamentos aprovados podem ser reembolsados")
	ErrRefundInvalidUser			 = errors.New("Usuário de cancelamento inválido")
	ErrPaymentInvalidStatus			 = errors.New("O pagamento não está pendente")
	ErrPaymentInvalidValue 			 = errors.New("O valor é inválido para o pagamento")
)

// Modelo de dados do pagamento
type Payment struct {
	ID     string
	OrderID string
	Amount float64
	Method PaymentMethod
	Status PaymentStatus
}

// Método para reembolsar o pagamento
func (p *Payment) Refund(user CancelUser) (float64, error) {
	if !PaymentIsApproved(p.Status) {
		return 0, ErrRefundInvalidStatus
	}

	refundPercent, err := GetRefundPercent(user)
	
	if err != nil {
		return 0, err
	}

	var refundAmount = p.Amount * refundPercent

	p.Status = PaymentRefunded
	// Futuramente: dispara evento para o RabbitMQ
	return refundAmount, nil
}

// Método para processar do pagamento
func (p *Payment) Process() error {
	if !PaymentIsPending(p.Status) {
		return ErrPaymentInvalidStatus
	}

	if !PaymentValueIsMoreThanZero(p.Amount) {
		return ErrPaymentInvalidValue
	}

	p.Status = PaymentApproved
	// Futuramente: dispara evento para o RabbitMQ
	return nil
}

// Função para verificar se o status do pagamento é APROVADO
func PaymentIsApproved(status PaymentStatus) bool {
	return status == PaymentApproved
}

// Função para verificar se o status do pagamento é PENDENTE
func PaymentIsPending(status PaymentStatus) bool {
	return status == PaymentPending
}

// Função para verificar se o valor do pagamento é maior que R$00,00
func PaymentValueIsMoreThanZero(amount float64) bool {
	return amount > 0
}

// Função para obter o percentual do valor total que será reembolsado
func GetRefundPercent(user CancelUser) (float64, error) {
	switch user {
		case CancelByUser:
			return 0.7, nil
		case CancelByStore:
			return 1, nil
		default:
			return 0, ErrRefundInvalidUser
	}
	
}