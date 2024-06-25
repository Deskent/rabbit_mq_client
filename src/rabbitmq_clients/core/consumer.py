import asyncio
from typing import Callable

from src.rabbitmq_clients.core.base_connect import BaseRabbitConnection


class RabbitConsumer(BaseRabbitConnection):
    async def consume(
        self,
        on_message_callback: Callable,
        queue_name: str = None,
    ):
        queue_name: str = self._get_queue_name(queue_name)
        async for channel in self.get_async_channel():
            queue = await channel.declare_queue(queue_name)
            await queue.consume(
                on_message_callback,
                no_ack=True,
            )
            await asyncio.Future()
