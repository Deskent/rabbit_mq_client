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
        self.__return_result_to = None

    async def consume(
        self,
        on_message_callback: typing.Callable,
        queue_name: str = None,
        auto_decode: bool = True,
    ):
        """Read messages from queue and send result to callback function.

        If queue_name is None - will be used self.queue_name.

        If auto_decode is True - decode and jsonify message before call
        callback function.
        If auto_decode is False - put message to callback function as is.

        """

        queue_name: str = self._get_queue_name(queue_name)
        self.__return_result_to = on_message_callback

        callback_handler: typing.Callable = (
            self.__consumer_callback if auto_decode else on_message_callback
        )

        async for channel in self.get_async_channel():
            queue = await channel.declare_queue(queue_name)
            await queue.consume(
                callback_handler,
                no_ack=True,
            )
            await asyncio.Future()

    async def __consumer_callback(
        self,
        message: aio_pika.message.AbstractIncomingMessage,
    ) -> None:
        encoded: str = message.body.decode()
        try:
            result: JSON = json.loads(encoded)
            await self.__return_result_to(result)
        except json.decoder.JSONDecodeError as err:
            raise RabbitConsumerJsonError(err)
