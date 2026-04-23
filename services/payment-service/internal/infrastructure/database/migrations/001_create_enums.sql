CREATE TYPE payment_status AS ENUM (
  'PENDENTE',
  'APROVADO',
  'REEMBOLSADO',
  'RECUSADO'
);

CREATE TYPE payment_method AS ENUM (
  'DEBITO',
  'CREDITO',
  'PIX'
);