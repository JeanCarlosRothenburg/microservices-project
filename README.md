# Descrição do Projeto

Este projeto foi desenvolvido como proposta para o primeiro trabalho da disciplina de DevOps.

A aplicação segue uma arquitetura de microsserviços, sendo composta por três APIs RESTful de domínio independentes, que comunicam-se entre si por meio de requisições HTTP.

---

## 📦 Libs utilizadas

### FastAPI

- Criação de endpoints HTTP para as APIs REST
- Autenticação entre os microsserviços

### PyJWT:

- Geração e validação de tokens JWT

### bcrypt

- Geração e validação de hash para senhas dos usuários

### email-validator

- Validação do formato do email informado para login

### pytest (only dev)

- Realização de testes unitários

### Black (only dev)

- formatador de código _opinated_ baseado no PEP 8

---

## Microsserviços de Domínio

### Usuário

Contém o domínio do negócio referente aos usuários do sistema.

#### Requisitos funcionais

| ID    | Descrição                                         |
| ----- | ------------------------------------------------- |
| RF-01 | O sistema deve permitir a autenticação no sistema |
| RF-02 | O sistema deve permitir o gerenciamento da conta  |

### Regras de negócio

| ID    | Descrição                                                    |
| ----- | ------------------------------------------------------------ |
| RN-01 | O sistema deve permitir o login com usuário e senha          |
| RN-02 | O usuário deve poder alterar o e-mail e a senha de sua conta |
| RN-03 | O usuário deve poder excluir sua conta                       |

## Pedido

## Estoque
