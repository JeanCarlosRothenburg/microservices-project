## Sumário

1. [Sobre o projeto](#sobre)
2. [Deploy local](#deploy-local)

# Sobre o projeto

## Objetivo do projeto

O projeto tem como objetivo aplicar os conhecimentos de **microsserviços**, **containerização** e **orquestração de containers** obtidos na disciplina de DevOps.

## Padrões de arquitetura de microsserviços

Foram aplicados dois padrões de arquitetura de microsserviços para a aplicação.

#### API-Gateway

**Objetivos**

- Fornecer um canal central de entrada para as requisições realizadas para a aplicação

- Realizar o roteamento para os microsserviços de domínio apropriados

- Realizar a autenticação através da validação do token JWT

  **Ferramenta:** Nginx

#### Choreography-based Saga

**Objetivos**

- Publicação de eventos em um message broker\_
- Gerenciar transações que envolvem múltiplos microsserviços
- Garantir a consistência dos dados caso ocorram falhas

**Ferramenta:** RabbitMQ

## Comunicação

A comunicação entre os microsserviços será estabelecida através de mensageria, utilizando a ferramenta RabbitMQ como **message broker** da aplicação.

## Microsserviços

O projeto conta com quatro microsserviços de domínio.

### Auth-Service

Microsserviço responsável pela autenticação do usuário e geração do token JWT para validação de requisições para outros microsserviços da aplicação.

**Arquitetura:** Camadas
**Linguagem:** Python
**Bibliotecas:** [PyJWT](https://pypi.org/project/PyJWT/) e [email-validator](https://pypi.org/project/email-validator/)

### Estoque

Microsserviço responsável por gerenciar o estoque.

**Arquitetura:** Camadas
**Linguagem:** Python
**Bibliotecas:** [FastAPI](https://pypi.org/project/fastapi/), [PyJWT](https://pypi.org/project/PyJWT/)
**Cobertura de testes:** Acima de 70%

**Requisitos funcionais**

| Identificador | Descrição                                              |
| :-----------: | :----------------------------------------------------- |
|     RF-01     | O sistema deve cadastrar produtos no estoque           |
|     RF-02     | O sistema deve listar e buscar produtos                |
|     RF-03     | O sistema deve atualizar a quantidade em estoque       |
|     RF-04     | O sistema deve verificar a disponibilidade de produtos |
|     RF-05     | O sistema deve remover produtos do estoque             |
|     RF-06     | O sistema deve atualizar os dados de um produto        |

**Regras de negócio**

| Identificador | Descrição                                     |
| :-----------: | :-------------------------------------------- |
|     RN-01     | A quantidade em estoque não pode ser negativa |
|     RN-02     | O preço do produto deve ser maior que R$0,00  |
|     RN-03     | O SKU deve ser único por produto              |

### Pedido

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

| Identificador | Descrição                                                                      |
| :-----------: | :----------------------------------------------------------------------------- |
|     RN-01     | Um pedido só pode ser criado se o usuário estiver autenticado                  |
|     RN-02     | O status inicial de todo pedido deve ser `PENDENTE`                            |
|     RN-03     | Um pedido só pode ser cancelado se estiver com status `PENDENTE` ou `APROVADO` |
|     RN-04     | Se o pagamento falhar, o pedido deve ser marcado como `CANCELADO`              |
|     RN-05     | Um pedido deve conter ao menos 1 item                                          |

### Payment-Service

Microsserviço responsável por processar pagamentos.

**Arquitetura:** Clean Architecture
**Tipo**: Event Driven
**Linguagem:** Golang
**Cobertura de testes:** 100% da lógica de negócio
**Bibliotecas**:

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

# Deploy local

Para realizar o deploy da aplicação localmente devem ser seguidos os passos abaixo:

1. Instalação do Docker

O Docker é necessário para o build das imagens e containerização no Kubernetes, portanto deve ser instalado e executado sua engine ou sua versão Desktop.

2. Buildar as imagens dos microsserviços:

O Kubernetes do projeto foi desenvolvido para utilizar as imagens locais para criação dos containers, portanto é necessário disponibilizá-las, sendo realizado através do comando:

```
cd <DIRETÓRIO_RAIZ_PROJETO>
docker build -t estoque-service:local services/estoque
docker build -t pedido-service:local services/pedido
docker build -t auth-service:local services/auth-service
```

2. Instalar o Kubernetes:

Para realizar o deploy da aplicação localmente e sua clusterização é necessário instalar as seguintes ferramentas do Kubernetes:

- Kubernetes CLI (kubectl)
- Minikube (simulador de cluster local)

3. Iniciar o Minikube:

```
minikube start --driver=docker
```

4. Instanciar os pods

```
cd <DIRETÓRIO_RAIZ_PROJETO>
kubectl apply -f k8s/auth-service
kubectl apply -f k8s/estoque-service
kubectl apply -f k8s/estoque-service/db
kubectl apply -f k8s/pedido-service
kubectl apply -f k8s/pedido-service/db
kubectl apply -f k8s/rabbitmq
kubectl apply -f k8s/monitoring/prometheus
kubectl apply -f k8s/monitoring/grafana
```

5. Iniciar tunnel

```
minikube tunnel
```

6. Definir os IPs externos lista de hosts local:

```
kubectl get ingress -A
```

O IP externo dos pods deve ser adicionado a lista de hosts local para resolver o DNS

- **Windows (CMD com privilégio de administrador):**

```

notepad C:\Windows\System32\drivers\etc\hosts

```

- **Linux/macOS:**

```

sudo nano /etc/hosts

```

Adicionar no arquivo os IPs externos dos hosts e seus nomes, obtidos no comando <code>kubectl get ingress -A<code>. Exemplo:

```
192.168.10.32 auth-service

```

7. Acessar os microsserviços no browser

```
kubectl get ingress
```

No navegador basta acessar o HOST definido na lista como domínio. Exemplo:

```
# Caso o host seja 'auth-service'
http://auth-service
```
