type Connection struct {
	conn *amqp.Connection
	channel *amqp.Channel
}