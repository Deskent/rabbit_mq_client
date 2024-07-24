### Stack:

- [x] <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-plain.svg" alt="python" width="15" height="15"/>
  Python 3.10+ <br/></a>
- [x] <a href="https://github.com/mosquito/aio-pika"><img src="https://raw.githubusercontent.com/mosquito/aio-pika/b61062893c4973dbbd5ac6a6afa55e4e74b28ae5/logo.svg" alt="aio-pika" width="15" height="15"/>
  aio-pika 9.4.1+ <br/></a>


### Installation

    pip install rabbitmq-clients

### Usage

    Run rabbitMQ on your computer.

#### Producer

    import asyncio
    import json

    from rabbitmq_clients import RabbitProducer

    if __name__ == "__main__":
        producer = RabbitProducer(
            host='localhost',
            login='test',
            password='test',
        )
        data = {"result": True}
        asyncio.run(
            producer.publish(
                json.dumps(data),
                queue_name='test_queue_name',
            )
        )


#### Consume multiply queues (recommended)

    import asyncio

    from rabbitmq_clients import RabbitConsumer, QueueDTO
    from rabbitmq_clients.core.types import JSON


    async def show_decoded_result(result: JSON):
        print(result)


    async def show_encoded_result(result: JSON):
        print(result.body)


    if __name__ == "__main__":
        consumer = RabbitConsumer(
            host='localhost',
            login='test',
            password='test',
        )
        first_queue = QueueDTO(
            name='decoded_result',
            callback=show_decoded_result,
        )
        second_queue = QueueDTO(
            name='encoded_result',
            callback=show_encoded_result,
            auto_decode=False,
        )
        consumer.add_queue(first_queue)
        consumer.add_queue(second_queue)

        try:
            asyncio.run(consumer.consume_all())
        except KeyboardInterrupt:
            pass
