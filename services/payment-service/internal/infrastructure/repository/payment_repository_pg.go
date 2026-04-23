package repository

import (
	"database/sql"
	"context"

	"github.com/JeanCarlosRothenburg/payment-service/internal/domain/entity"
)

type PaymentRepositoryPostgreSQL struct {
	db *sql.DB
}

func NewPaymentRepository(db *sql.DB) *PaymentRepositoryPostgreSQL {
	return &PaymentRepositoryPostgreSQL{db: db}
}

func (r *PaymentRepositoryPostgreSQL) Save(ctx context.Context, p entity.Payment) error {
	_, err := r.db.ExecContext(ctx,
	`INSERT INTO payment (order_id, amount, status, method)
	 VALUES ($1, $2, $3, $4)`,
	p.OrderID, p.Amount, p.Status, p.Method)

	return err
}

func (r *PaymentRepositoryPostgreSQL) FindByID(ctx context.Context, id string) (*entity.Payment, error) {
	row := r.db.QueryRowContext(ctx,
	`SELECT id, order_id, amount, method, status
	   FROM payment
	  WHERE id = $1`,
	id)

	var p entity.Payment

	err := row.Scan(
		&p.ID,
		&p.OrderID,
		&p.Amount,
		&p.Method,
		&p.Status
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	return &p, nil
}