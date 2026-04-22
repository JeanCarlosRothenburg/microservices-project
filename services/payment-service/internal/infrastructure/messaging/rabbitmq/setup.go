package rabbitmq

import amqp "github.com/rabbitmq/amqp091-go"

func setup(ch *amqp.Channel) error {
	err := ch.ExchangeDeclare(
		"dlx.exchange", "direct", true, false, false, false, nil,
	)

	if err != nil {
		return err
	}

	dlxArgs := amqp.Table{"x-dead-letter-exchange": "dlx.exchange"}

	_, err = ch.QueueDeclare(
		"payment.queue", true, false, false, false, dlxArgs,
	)

	if err != nil {
		return err
	}

	queues := []string{"payment.approved", "payment.failed"}

	for _, queue := range queues {
		_, err = ch.QueueDeclare(
			queue, true, false, false, false, nil,
		)

		if err != nil {
			return err
		}
	}

	return nil
}