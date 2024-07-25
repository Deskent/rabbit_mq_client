import json

from aio_pika.abc import AbstractIncomingMessage, AbstractQueue

from rabbitmq_clients import RabbitConsumer, RabbitProducer


async def test_consumer_get_connection(
    consumer: RabbitConsumer,
) -> None:
    async with consumer.get_async_connection() as connection:
        assert connection is not None


async def test_consumer_get_channel(
    consumer: RabbitConsumer,
) -> None:
    async with consumer.get_async_channel() as channel:
        assert channel is not None


async def test_consumer_get_message_from_channel(
    producer: RabbitProducer,
    consumer: RabbitConsumer,
    dataset: dict,
    queue_name: str,
) -> None:
    message: str = json.dumps(dataset)
    await producer.publish(message=message, queue_name=queue_name)

    async with consumer.get_async_channel() as channel:
        queue: AbstractQueue = await channel.declare_queue(queue_name)
        received_message: AbstractIncomingMessage = await queue.get(
            no_ack=True
        )
        assert received_message.body.decode() == message
