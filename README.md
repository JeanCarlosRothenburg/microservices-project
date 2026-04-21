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

**Arquitetura:** Camadas
**Linguagem:** Python
**Bibliotecas:** [FastAPI](https://pypi.org/project/fastapi/), [PyJWT](https://pypi.org/project/PyJWT/)
**Cobertura de testes:** Acima de 70%

**Requisitos funcionais**

| Identificador | Descrição                                               |
| :-----------: | :------------------------------------------------------ |
|     RF-01     | O sistema deve cadastrar produtos no estoque            |
|     RF-02     | O sistema deve listar e buscar produtos                 |
|     RF-03     | O sistema deve atualizar a quantidade em estoque        |
|     RF-04     | O sistema deve verificar a disponibilidade de produtos  |
|     RF-05     | O sistema deve remover produtos do estoque              |
|     RF-06     | O sistema deve atualizar os dados de um produto         |

**Regras de negócio**

| Identificador | Descrição                                                                                 |
| :-----------: | :---------------------------------------------------------------------------------------- |
|     RN-01     | A quantidade em estoque não pode ser negativa                                             |
|     RN-02     | O preço do produto deve ser maior que R$0,00                                              |
|     RN-03     | O SKU deve ser único por produto                                                          |

## Pedido

Microsserviço responsável por processar pedidos, coordenando a verificação de estoque e o processamento de pagamento via requisições REST.

**Arquitetura:** Camadas
**Linguagem:** Python
**Bibliotecas:** [FastAPI](https://pypi.org/project/fastapi/), [PyJWT](https://pypi.org/project/PyJWT/), [httpx](https://pypi.org/project/httpx/)
**Cobertura de testes:** Acima de 75%

**Requisitos funcionais**

| Identificador | Descrição                                      |
| :-----------: | :--------------------------------------------- |
|     RF-01     | O sistema deve criar um pedido                 |
|     RF-02     | O sistema deve cancelar um pedido              |
|     RF-03     | O sistema deve consultar o status de um pedido |
|     RF-04     | O sistema deve listar os pedidos do usuário    |

**Regras de negócio**

| Identificador | Descrição                                                                       |
| :-----------: | :------------------------------------------------------------------------------ |
|     RN-01     | Um pedido só pode ser criado se o usuário estiver autenticado                   |
|     RN-02     | O status inicial de todo pedido deve ser `PENDENTE`                             |
|     RN-03     | Um pedido só pode ser cancelado se estiver com status `PENDENTE` ou `APROVADO`  |
|     RN-04     | Se o pagamento falhar, o pedido deve ser marcado como `CANCELADO`               |
|     RN-05     | Um pedido deve conter ao menos 1 item                                           |

## Payment-Service

Microsserviço responsável por processar pagamentos.

**Arquitetura:** Clean Architecture
**Linguagem:** Golang
**Cobertura de testes:** 100%

**Requisitos funcionais**

| Identificador | Descrição                                      |
| :-----------: | :--------------------------------------------- |
|     RF-01     | O sistema deve processar pagamentos de pedidos |
|     RF-02     | O sistema deve reembolsar pagamentos           |

**Regras de negócio**

| Identificador | Descrição                                                                                      |
| :-----------: | :--------------------------------------------------------------------------------------------- |
|     RN-01     | O pagamento deve ser processado somente se o valor do pedido for maior que R$00,00             |
|     RN-02     | O pagamento deve ser processado somente se o valor do pedido estiver com o status `PENDENTE`   |
|     RN-03     | Para pagamentos com cartão deve ser validado o número do cartão                                |
|     RN-04     | Pagamentos devem ser reembolsados somente se o status do pedido for `APROVADO`                 |
|     RN-05     | Para cancelamentos efetuados por usuários o reembolso será de 70% do valor total do pedido     |
|     RN-06     | Para cancelamento efetuados pela loja o reembolso será correspondente ao valor total do pedido |
