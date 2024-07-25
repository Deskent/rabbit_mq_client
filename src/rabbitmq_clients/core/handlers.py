import json
import typing

from aio_pika.abc import AbstractIncomingMessage

from rabbitmq_clients.core.exceptions import RabbitConsumerJsonError
from rabbitmq_clients.core.types import JSON


class CallbackHandler:
    """Class for handling queue consumed data.
    :param callback: callback function will be called when data is received.

    :param auto_decode: automatically decode JSON data.
    """

    def __init__(
        self,
        callback: typing.Callable,
        auto_decode: bool = True,
    ) -> None:

        self._callback = callback
        self._auto_decode = auto_decode

    async def __decode_and_callback_result(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        encoded: str = message.body.decode()
        try:
            result: JSON = json.loads(encoded)
            return await self._callback(result)
        except json.decoder.JSONDecodeError as err:
            raise RabbitConsumerJsonError(err)

    async def handle(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> JSON | AbstractIncomingMessage:
        """Handle a message using the callback handler."""

        if self._auto_decode:
            return await self.__decode_and_callback_result(*args, **kwargs)

        return await self._callback(*args, **kwargs)
