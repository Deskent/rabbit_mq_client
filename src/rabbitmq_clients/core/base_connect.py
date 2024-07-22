from typing import AsyncGenerator

import aio_pika


class BaseRabbitConnection:
    def __init__(
        self,
        host: str,
        login: str,
        password: str,
        queue_name: str = "",
        exchange_name: str = "",
        routing_key: str = "",
    ):
        """Base connection class for RabbitMQ clients.

        Attributes:

            host: str - RabbitMQ hostname

            login: str - RabbitMQ username

            password: str - RabbitMQ password

            queue_name: str = '' - RabbitMQ default queue name

            exchange_name: str = '' - RabbitMQ default exchange name

            routing_key: str = '' - RabbitMQ default routing key

        """
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.host = host
        self.login = login
        self.password = password

    async def get_async_connection(
        self,
    ) -> AsyncGenerator[aio_pika.abc.AbstractConnection, None]:
        connection = await aio_pika.connect(
            host=self.host,
            login=self.login,
            password=self.password,
        )
        yield connection

    async def get_async_channel(
        self,
    ) -> AsyncGenerator[aio_pika.abc.AbstractChannel, None]:
        async for connection in self.get_async_connection():
            channel: aio_pika.abc.AbstractChannel = await connection.channel()
            yield channel

    def _validate_queue_name(self, queue_name: str) -> str:
        queue_name: str = queue_name if queue_name else self.queue_name
        if queue_name:
            return queue_name
        raise ValueError("Queue name cannot be empty")
