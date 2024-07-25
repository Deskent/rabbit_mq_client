import contextlib
from typing import AsyncGenerator

import aio_pika


class BaseRabbitConnection:
    def __init__(
        self,
        login: str,
        password: str,
        host: str,
        port: int = 5672,
        queue_name: str = "",
        exchange_name: str = "",
        routing_key: str = "",
    ):
        """Base connection class for RabbitMQ clients.

        Attributes:

            host: str - RabbitMQ hostname

            port: int = 5672 - RabbitMQ port

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
        self.port = port
        self.login = login
        self.password = password

    @contextlib.asynccontextmanager
    async def get_async_connection(
        self,
    ) -> AsyncGenerator[aio_pika.abc.AbstractConnection, None]:
        connection = await aio_pika.connect(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
        )
        yield connection

    @contextlib.asynccontextmanager
    async def get_async_channel(
        self,
    ) -> AsyncGenerator[aio_pika.abc.AbstractChannel, None]:
        async with self.get_async_connection() as connection:
            channel: aio_pika.abc.AbstractChannel = await connection.channel()
            yield channel

    def _validate_queue_name(self, queue_name: str) -> str:
        queue_name: str = queue_name if queue_name else self.queue_name
        if queue_name:
            return queue_name
        raise ValueError("Queue name cannot be empty")
