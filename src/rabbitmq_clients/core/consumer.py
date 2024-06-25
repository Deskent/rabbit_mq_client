import asyncio
import json
import typing

import aio_pika

from .base_connect import BaseRabbitConnection
from .exceptions import RabbitConsumerJsonError
from .types import JSON


class RabbitConsumer(BaseRabbitConnection):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.return_result_to = None

    async def consume(
        self,
        on_message_callback: typing.Callable,
        queue_name: str = None,
    ):
        queue_name: str = self._get_queue_name(queue_name)
        self.return_result_to = on_message_callback

        async for channel in self.get_async_channel():
            queue = await channel.declare_queue(queue_name)
            await queue.consume(
                self.__consumer_callback,
                no_ack=True,
            )
            await asyncio.Future()

    async def __consumer_callback(
        self, message: aio_pika.message.AbstractIncomingMessage
    ) -> None:
        encoded: str = message.body.decode()
        try:
            result: JSON = json.loads(encoded)
            await self.return_result_to(result)
        except json.decoder.JSONDecodeError as err:
            raise RabbitConsumerJsonError(err)
