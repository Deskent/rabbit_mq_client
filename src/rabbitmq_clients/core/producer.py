import contextlib
from typing import AsyncGenerator

import aio_pika

from .base_connect import BaseRabbitConnection


class RabbitProducer(BaseRabbitConnection):
    @contextlib.asynccontextmanager
    async def get_async_connection(
        self,
    ) -> AsyncGenerator[aio_pika.abc.AbstractConnection, None]:
        """Close connection after publish."""

        connection = await aio_pika.connect(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
        )
        yield connection
        await connection.close()

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
