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

    from rabbitmq-clients import RabbitProducer

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
    import json

    import aio_pika

    from rabbitmq-clients import RabbitConsumer


    async def on_message_callback(message: aio_pika.IncomingMessage):
        encoded: str = message.body.decode()
        try:
            jsoned: dict = json.loads(encoded)
            print(f"Received message: {jsoned}")
        except json.decoder.JSONDecodeError as err:
            print(err)
            print(f"Received message: {encoded}")


    if __name__ == "__main__":
        consumer = RabbitConsumer(
            host='localhost',
            login='test',
            password='test',
            queue_name='test_queue',
            exchange_name='',
            routing_key='',
        )
        try:
            asyncio.run(consumer.consume(on_message_callback=on_message_callback))
        except KeyboardInterrupt:
            pass
