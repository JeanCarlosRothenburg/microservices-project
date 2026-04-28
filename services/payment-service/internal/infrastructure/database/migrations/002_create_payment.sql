CREATE TABLE payment (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id UUID NOT NULL,
    amount NUMERIC NOT NULL,
    status payment_status NOT NULL DEFAULT 'PENDENTE',
    method payment_method NOT NULL
)