import aio_pika

from .base_connect import BaseRabbitConnection


class RabbitProducer(BaseRabbitConnection):
    async def publish(
        self,
        message: str,
        queue_name: str = "",
    ) -> None:
        """Publish message to RabbitMQ queue."""

        queue_name: str = self._validate_queue_name(queue_name)
        async with self.get_async_channel() as channel:
            queue = await channel.declare_queue(queue_name)

            exchange = channel.default_exchange
            if self.exchange_name:
                exchange = await channel.declare_exchange(self.exchange_name)

            await exchange.publish(
                message=aio_pika.Message(body=message.encode()),
                routing_key=queue.name,
            )
