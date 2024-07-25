import asyncio
import logging
import typing
import warnings

from aio_pika.abc import AbstractQueue

from .base_connect import BaseRabbitConnection
from .dto import QueueDTO
from .handlers import CallbackHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class RabbitConsumer(BaseRabbitConnection):
    """Class for consuming messages from RabbitMQ queues.

    :param auto_decode: bool = True
        - Automatically decode JSON data if True.

    :param no_ack: bool = True

    Methods:
        consume_all - Consume all messages from self queues.

    """

    def __init__(
        self,
        auto_decode: bool = True,
        no_ack: bool = True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._queues: dict[str, QueueDTO] = {}
        self._auto_decode = auto_decode
        self._no_ack = no_ack

    def add_queue(self, new_queue: QueueDTO) -> int:
        self._queues[new_queue.name] = new_queue

        return len(self._queues)

    def remove_queue(self, name: str) -> QueueDTO:
        if name not in self._queues:
            raise ValueError(f'Queue {name} not found.')

        return self._queues.pop(name)

    def show_queues(self) -> dict[str, QueueDTO]:
        return self._queues

    async def consume_all(self) -> None:
        """Start consuming from all queues."""

        logger.debug(f'Start consuming from {len(self._queues)} queues')
        for queue_name, queue in self._queues.items():
            await self._consume_from_queue(
                queue_name=queue.name,
                on_message_callback=queue.callback,
                auto_decode=queue.auto_decode,
                no_ack=queue.no_ack,
            )
        await asyncio.Future()

    async def _consume_from_queue(
        self,
        queue_name: str,
        on_message_callback: typing.Callable,
        auto_decode: bool = True,
        no_ack: bool = True,
    ) -> None:
        """Consume one queue."""

        queue_name: str = self._validate_queue_name(queue_name)

        callback_handler: CallbackHandler = CallbackHandler(
            callback=on_message_callback,
            auto_decode=auto_decode,
        )

        async with self.get_async_channel() as channel:
            queue: AbstractQueue = await channel.declare_queue(queue_name)
            await queue.consume(
                callback_handler.handle,
                no_ack=no_ack,
            )

    async def consume(
        self,
        on_message_callback: typing.Callable,
        queue_name: str = None,
        auto_decode: bool = True,
        no_ack: bool = True,
    ):
        """
        Deprecated and will be removed in version 0.2.0!

        Read messages from queue and send result to callback function.

        If queue_name is None - will be used self.queue_name.

        If auto_decode is True - decode and jsonify message before call
        callback function.

        If auto_decode is False - put message to callback function as is.


        """
        warnings.warn(
            'This method deprecated and will be removed in version 0.2.0. '
            'Please use method "consume_all".',
            DeprecationWarning,
        )
        await self._consume_from_one_queue(
            queue_name,
            on_message_callback,
            auto_decode,
            no_ack,
        )

    async def _consume_from_one_queue(
        self,
        queue_name: str,
        on_message_callback: typing.Callable,
        auto_decode: bool = True,
        no_ack: bool = True,
    ) -> None:
        """Deprecated and will be removed in version 0.2.0!

        Consume one queue.
        """

        queue_name: str = self._validate_queue_name(queue_name)

        callback_handler: CallbackHandler = CallbackHandler(
            callback=on_message_callback,
            auto_decode=auto_decode,
        )

        async for channel in self.get_async_channel():
            queue: AbstractQueue = await channel.declare_queue(queue_name)
            await queue.consume(
                callback_handler.handle,
                no_ack=no_ack,
            )
            await asyncio.Future()
