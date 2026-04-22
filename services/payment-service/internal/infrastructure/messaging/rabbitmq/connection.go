package rabbitmq

import (
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
)

type Connection struct {
	conn *amqp.Connection
	channel *amqp.Channel
	url string
}

func NewConnection() *Connection {
	url, exists := os.LookupEnv("RABBITMQ_URL")

	if !exists {
		log.Fatal("A constante da URL do RabbitMQ URL não foi encontrada!")
	}

	c := &Connection{url: url}
	c.connect()
	return c

}

func (c *Connection) connect() {
	conn, err := amqp.Dial(c.url)
	if err != nil {
		log.Fatal("Não foi possível estabelecer a conexão com o RabbitMQ")
	}

	channel, err := conn.Channel()
	if err != nil {
		conn.Close()
		log.Fatal("Não foi possível abrir uma canal no RabbitMQ")
	}

	c.conn = conn
	c.channel = channel

	err = setup(channel)
	if err != nil {
		log.Fatal("Erro ao configurar topologia do RabbitMQ")
	}
}

func (c *Connection) Channel() *amqp.Channel {
	if c.channel == nil || c.channel.IsClosed() {
		channel, err := c.conn.Channel()
		if err != nil {
			log.Println("Erro ao abrir canal no RabbitMQ!")
			c.connect()
			return c.channel
		}
		log.Println("Canal aberto no RabbitMQ!")
		c.channel = channel

	}

	log.Println("Já existe um canal aberto no RabbitMQ!")
	return c.channel
}

func (c *Connection) Close() {
	if c.channel != nil && !c.channel.IsClosed() {
		c.channel.Close()
	}
	if c.conn != nil && !c.conn.IsClosed() {
		c.conn.Close()
	}
	log.Println("Conexão com o RabbitMQ encerrada!")
}