# Objetivo do projeto

O projeto tem como objetivo aplicar os conhecimentos de **microsserviços**, **containerização** e **orquestração de containers** obtidos na disciplina de DevOps.

# Padrões de arquitetura de microsserviços

Foram aplicados dois padrões de arquitetura de microsserviços para a aplicação.

### API-Gateway

**Objetivos**

- Fornecer um canal central de entrada para as requisições realizadas para a aplicação

- Realizar o roteamento para os microsserviços de domínio apropriados

- Realizar a autenticação através da validação do token JWT

  **Ferramenta:** Nginx

### Choreography-based Saga

**Objetivos**

- Publicação de eventos em um _message broker_
- Gerenciar transações que envolvem múltiplos microsserviços
- Garantir a consistência dos dados caso ocorram falhas

**Ferramenta:** RabbitMQ

# Comunicação

A comunicação entre os microsserviços será estabelecida obedecendo a arquitetura REST, através de requisições seguindo o protocolo HTTP.

# Microsserviços

O projeto conta com quatro microsserviços de domínio.

## Auth-Service

Microsserviço responsável pela autenticação do usuário e geração do token JWT para validação de requisições para outros microsserviços da aplicação.

**Arquitetura:** Camadas
**Linguagem:** Python
**Bibliotecas:** [bcrypt](https://pypi.org/project/bcrypt/), [PyJWT](https://pypi.org/project/PyJWT/) e [email-validator](https://pypi.org/project/email-validator/)

## Estoque

Microsserviço responsável por gerenciar o estoque.

## Pedido

Microsserviço responsável por processar pedidos

## Pagamento

Microsserviço responsável por processar pagamentos
