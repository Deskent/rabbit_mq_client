import dataclasses
import json

import aio_pika

from rabbitmq_clients.core.handlers import CallbackHandler
from rabbitmq_clients.core.types import JSON


@dataclasses.dataclass
class TestAbstractMessage:
    body: bytes


async def callback_for_decoded(result: JSON):
    return result


async def callback_for_not_decoded(
    result: aio_pika.abc.AbstractIncomingMessage,
):
    return result


async def test_callback_handler_with_auto_decode(
    dataset: dict,
) -> None:
    handler = CallbackHandler(
        callback=callback_for_decoded,
        auto_decode=True,
    )
    message = TestAbstractMessage(body=json.dumps(dataset).encode())
    handled_message: JSON = await handler.handle(message)
    assert handled_message == dataset


async def test_callback_handler_without_auto_decode(
    dataset: dict,
) -> None:
    handler = CallbackHandler(
        callback=callback_for_not_decoded,
        auto_decode=False,
    )
    message = TestAbstractMessage(body=json.dumps(dataset).encode())
    handled_message: TestAbstractMessage = await handler.handle(message)
    assert json.loads(handled_message.body.decode()) == dataset
