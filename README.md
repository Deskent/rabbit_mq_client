### Stack:

- [x] <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-plain.svg" alt="python" width="15" height="15"/>
  Python 3.11+ <br/></a>
- [x] <a href="https://github.com/mosquito/aio-pika"><img src="https://raw.githubusercontent.com/mosquito/aio-pika/b61062893c4973dbbd5ac6a6afa55e4e74b28ae5/logo.svg" alt="aio-pika" width="15" height="15"/>
  aio-pika 9.4.1+ <br/>

### Installation

    pip install rabbitmq-clients

### Usage

#### Producer

    import asyncio
    import json

    from rabbitmq_clients import RabbitProducer

    if __name__ == "__main__":
        publisher = RabbitProducer(
            host='localhost',
            login='test',
            password='test',
            queue_name='test_queue',
            exchange_name='',
            routing_key='',
        )
        data = {"result": True}
        asyncio.run(publisher.publish(json.dumps(data)))

#### Consumer

    import asyncio

    from rabbitmq_clients import RabbitConsumer
    from rabbitmq_clients.core.types import JSON


    async def show_result(result: JSON):
        print(result)


    if __name__ == "__main__":
        consumer = RabbitConsumer(
            host='localhost',
            login='test',
            password='test',
            queue_name='test_queue',
        )
        try:
            asyncio.run(consumer.consume(on_message_callback=show_result))
        except KeyboardInterrupt:
            pass
